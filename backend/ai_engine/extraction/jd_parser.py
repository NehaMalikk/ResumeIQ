"""Deterministic job-description structure extraction."""

from __future__ import annotations

import logging
import re
from collections.abc import Iterable

from ai_engine.extraction.categories import categorize
from ai_engine.extraction.jd_constants import BULLET_PREFIXES, EMPLOYMENT_TYPES, JD_SECTION_ALIASES, MAX_JD_HEADING_LENGTH
from ai_engine.extraction.jd_models import JobBenefit, JobDescription, JobRequirement, JobResponsibility, JobSkill
from ai_engine.extraction.jd_patterns import EMAIL_PATTERN, EXPERIENCE_PATTERN, KEYWORD_PHRASE_PATTERN, SALARY_PATTERN, URL_PATTERN
from ai_engine.extraction.skill_extractor import SkillExtractor

logger = logging.getLogger(__name__)


class JobDescriptionParser:
    """Safely convert plain extracted JD text into a :class:`JobDescription`."""

    def __init__(self, skill_extractor: SkillExtractor | None = None) -> None:
        self._skill_extractor = skill_extractor or SkillExtractor()

    def parse(self, text: str) -> JobDescription:
        """Return the best structured result possible; never raise for bad input."""
        logger.info("Job description parsing started")
        if not isinstance(text, str):
            logger.warning("Job description parsing received non-string input")
            return JobDescription(raw_text="")
        normalized = self._normalize_text(text)
        if not normalized:
            logger.warning("Job description parsing received empty text")
            return JobDescription(raw_text="")
        try:
            sections, preamble = self._detect_sections(normalized)
            logger.info("Job description sections detected: %s", ", ".join(sections) or "none")
            required_text = self._section_text(sections, "required_skills", "requirements")
            preferred_text = self._section_text(sections, "preferred_skills")
            nice_text = self._section_text(sections, "nice_to_have_skills")
            required_skills = self._skills(required_text)
            preferred_skills = self._skills(preferred_text, exclude=required_skills)
            nice_skills = self._skills(nice_text, exclude=[*required_skills, *preferred_skills])
            logger.info("Skills extracted: required=%d preferred=%d nice_to_have=%d", len(required_skills), len(preferred_skills), len(nice_skills))
            responsibilities = self._items(sections.get("responsibilities", []), JobResponsibility)
            logger.info("Responsibilities extracted: %d", len(responsibilities))
            all_text = "\n".join([preamble, *["\n".join(lines) for lines in sections.values()]])
            result = JobDescription(
                title=self._first_value(sections.get("title", [])) or self._title_from_preamble(preamble),
                company=self._first_value(sections.get("company", [])),
                location=self._first_value(sections.get("location", [])) or self._location_from_text(all_text),
                employment_type=self._first_value(sections.get("employment_type", [])) or self._employment_type_from_text(all_text),
                department=self._first_value(sections.get("department", [])),
                experience_required=self._first_match(EXPERIENCE_PATTERN, self._section_text(sections, "experience", "requirements", "qualifications")) or self._first_match(EXPERIENCE_PATTERN, all_text),
                education_required=self._first_value(sections.get("education", [])) or self._education_from_text(all_text),
                required_skills=required_skills,
                preferred_skills=preferred_skills,
                nice_to_have_skills=nice_skills,
                responsibilities=responsibilities,
                qualifications=self._items([*sections.get("qualifications", []), *sections.get("requirements", [])], JobRequirement),
                benefits=self._items(sections.get("benefits", []), JobBenefit),
                certifications=self._content_lines(sections.get("certifications", [])),
                salary=self._first_value(sections.get("salary", [])) or self._first_match(SALARY_PATTERN, all_text),
                keywords=self._keywords(all_text, [*required_skills, *preferred_skills, *nice_skills]),
                urls=self._deduplicate(URL_PATTERN.findall(all_text)),
                emails=self._deduplicate(EMAIL_PATTERN.findall(all_text)),
                raw_text=text,
            )
            logger.info("Job description parsing completed")
            return result
        except Exception:
            logger.exception("Job description parsing failed; returning partial empty result")
            return JobDescription(raw_text=text)

    def _detect_sections(self, text: str) -> tuple[dict[str, list[str]], str]:
        sections: dict[str, list[str]] = {}
        preamble: list[str] = []
        current: str | None = None
        for line in text.splitlines():
            section, remainder = self._heading(line)
            if section:
                current = section
                sections.setdefault(section, [])
                if remainder:
                    sections[section].append(remainder)
            elif current is None:
                preamble.append(line)
            else:
                sections[current].append(line)
        return sections, "\n".join(preamble)

    @staticmethod
    def _heading(line: str) -> tuple[str | None, str]:
        stripped = line.strip()
        candidate = re.sub(r"\s+", " ", stripped.rstrip(":").strip())
        key = candidate.casefold()
        if len(key) <= MAX_JD_HEADING_LENGTH and key in JD_SECTION_ALIASES:
            return JD_SECTION_ALIASES[key], ""
        inline = re.match(r"^\s*([^:]{1,80})\s*:\s*(.+?)\s*$", line)
        if inline:
            key = re.sub(r"\s+", " ", inline.group(1).strip()).casefold()
            if key in JD_SECTION_ALIASES:
                return JD_SECTION_ALIASES[key], inline.group(2)
        return None, ""

    def _skills(self, text: str, exclude: Iterable[JobSkill] = ()) -> list[JobSkill]:
        ignored = {skill.name for skill in exclude}
        return [JobSkill(name=name, category=category) for name in self._skill_extractor.extract(text) if name not in ignored and (category := categorize(name))]

    @staticmethod
    def _items(lines: list[str], model: type[JobRequirement] | type[JobResponsibility] | type[JobBenefit]) -> list[JobRequirement] | list[JobResponsibility] | list[JobBenefit]:
        return [model(text=value) for value in JobDescriptionParser._content_lines(lines)]

    @staticmethod
    def _content_lines(lines: Iterable[str]) -> list[str]:
        values: list[str] = []
        for line in lines:
            cleaned = line.strip().lstrip("".join(BULLET_PREFIXES)).strip()
            cleaned = re.sub(r"^\d+[.)]\s*", "", cleaned)
            if cleaned:
                values.append(cleaned)
        return JobDescriptionParser._deduplicate(values)

    @staticmethod
    def _section_text(sections: dict[str, list[str]], *names: str) -> str:
        return "\n".join(line for name in names for line in sections.get(name, []))

    @staticmethod
    def _first_value(lines: list[str]) -> str | None:
        values = JobDescriptionParser._content_lines(lines)
        return " ".join(values) if values else None

    @staticmethod
    def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
        match = pattern.search(text)
        return match.group(0).strip() if match else None

    @staticmethod
    def _title_from_preamble(preamble: str) -> str | None:
        for line in JobDescriptionParser._content_lines(preamble.splitlines())[:3]:
            if not EMAIL_PATTERN.search(line) and not URL_PATTERN.search(line) and len(line) <= 100:
                return line
        return None

    @staticmethod
    def _employment_type_from_text(text: str) -> str | None:
        match = re.search(r"\b(?:" + "|".join(re.escape(value) for value in EMPLOYMENT_TYPES) + r")\b", text, re.IGNORECASE)
        return match.group(0).title() if match else None

    @staticmethod
    def _location_from_text(text: str) -> str | None:
        match = re.search(r"\b(?:remote|hybrid|on[- ]site)\b", text, re.IGNORECASE)
        return match.group(0).title() if match else None

    @staticmethod
    def _education_from_text(text: str) -> str | None:
        match = re.search(r"\b(?:bachelor(?:'s)?|master(?:'s)?|ph\.?d\.?|b\.?tech|b\.?sc|m\.?sc)\b[^\n.]*", text, re.IGNORECASE)
        return match.group(0).strip() if match else None

    @staticmethod
    def _keywords(text: str, skills: Iterable[JobSkill]) -> list[str]:
        phrases = [match.group(0) for match in KEYWORD_PHRASE_PATTERN.finditer(text)]
        return JobDescriptionParser._deduplicate([*(skill.name for skill in skills), *phrases])

    @staticmethod
    def _normalize_text(text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n").strip()

    @staticmethod
    def _deduplicate(values: Iterable[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            cleaned = value.strip()
            if cleaned and cleaned.casefold() not in seen:
                seen.add(cleaned.casefold())
                result.append(cleaned)
        return result


# Compatibility with the pre-Milestone-4 public name.
JDParser = JobDescriptionParser
