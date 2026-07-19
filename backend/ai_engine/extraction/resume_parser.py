"""Deterministic parsing of extracted resume text into :mod:`models` objects."""

from __future__ import annotations

import logging
import re
from collections.abc import Iterable

from ai_engine.extraction.constants import BULLET_PREFIXES, MAX_HEADING_LENGTH, SECTION_ALIASES, SECTION_NAMES
from ai_engine.extraction.models import (
    PersonalInfo,
    Resume,
    ResumeCertification,
    ResumeEducation,
    ResumeExperience,
    ResumeLanguage,
    ResumeProject,
    ResumeSkill,
)
from ai_engine.extraction.patterns import DATE_RANGE_PATTERN, DATE_PATTERN, EMAIL_PATTERN, GITHUB_PATTERN, LINKEDIN_PATTERN, PHONE_PATTERN, URL_PATTERN
from ai_engine.extraction.categories import categorize
from ai_engine.extraction.skill_extractor import SkillExtractor

logger = logging.getLogger(__name__)


class ResumeParser:
    """Convert plain UTF-8 resume text into a structured :class:`Resume`.

    The parser is intentionally heuristic and deterministic. It identifies
    conventional headings and preserves ambiguous content instead of making
    unsupported semantic inferences.
    """

    def __init__(self, skill_extractor: SkillExtractor | None = None) -> None:
        self._skill_extractor = skill_extractor or SkillExtractor()

    def parse(self, text: str) -> Resume:
        """Parse ``text`` safely, returning empty fields when data is absent."""
        logger.info("Resume parsing started")
        if not isinstance(text, str):
            logger.warning("Resume parsing received non-string input")
            return Resume(raw_text="")

        normalized = self._normalize_text(text)
        if not normalized:
            logger.warning("Resume parsing received empty text")
            return Resume(raw_text="")

        sections, preamble = self._detect_sections(normalized)
        logger.info("Resume sections detected: %s", ", ".join(sections) or "none")
        missing = SECTION_NAMES - set(sections)
        if missing:
            logger.info("Resume sections missing: %s", ", ".join(sorted(missing)))

        resume = Resume(
            personal_info=self.extract_personal_info(preamble or normalized),
            summary=self.extract_summary(sections.get("summary", [])),
            # Technologies demonstrated in work and projects are valid evidence,
            # not merely those repeated under a conventional Skills heading.
            skills=self.extract_skills(normalized.splitlines()),
            experience=self.extract_experience(sections.get("experience", [])),
            projects=self.extract_projects(sections.get("projects", [])),
            education=self.extract_education(sections.get("education", [])),
            certifications=self.extract_certifications(sections.get("certifications", [])),
            languages=self.extract_languages(sections.get("languages", [])),
            raw_text=text,
        )
        logger.info("Resume parsing completed")
        return resume

    def extract_personal_info(self, text: str) -> PersonalInfo:
        """Extract header contact details using conservative regular expressions."""
        lines = [line for line in text.splitlines() if line.strip()]
        header = "\n".join(lines[:8])
        email = self._first_match(EMAIL_PATTERN, header)
        phone = self._first_match(PHONE_PATTERN, header)
        linkedin = self._first_match(LINKEDIN_PATTERN, header)
        github = self._first_match(GITHUB_PATTERN, header)
        urls = URL_PATTERN.findall(header)
        portfolio = next((url for url in urls if "linkedin.com" not in url.lower() and "github.com" not in url.lower()), None)
        name = self._extract_name(lines, email, phone)
        return PersonalInfo(name=name, email=email, phone=phone, linkedin=linkedin, github=github, portfolio=portfolio)

    def extract_summary(self, lines: list[str]) -> str | None:
        """Return a whitespace-normalized professional summary."""
        value = " ".join(self._content_lines(lines))
        return value or None

    def extract_skills(self, lines: list[str]) -> list[ResumeSkill]:
        """Extract normalized, categorized skills from the skills section."""
        skills = self._skill_extractor.extract("\n".join(self._content_lines(lines)))
        result = [ResumeSkill(name=skill, category=category) for skill in skills if (category := categorize(skill))]
        logger.info("Skill categories assigned: %s", ", ".join(item.category for item in result) or "none")
        return result

    def extract_raw_skills(self, lines: list[str]) -> list[str]:
        """Split source skill lines; retained for callers needing raw text."""
        values: list[str] = []
        for line in self._content_lines(lines):
            cleaned = re.sub(r"^(?:skills?|technologies)\s*:\s*", "", line, flags=re.IGNORECASE)
            values.extend(part.strip() for part in re.split(r"[,;|•]+", cleaned) if part.strip())
        return self._deduplicate(values)

    def extract_experience(self, lines: list[str]) -> list[ResumeExperience]:
        """Parse blank-line/date-delimited work entries."""
        return [self._experience_from_block(block) for block in self._blocks(lines) if block]

    def extract_projects(self, lines: list[str]) -> list[ResumeProject]:
        """Parse project blocks, retaining descriptive bullets and URLs."""
        projects: list[ResumeProject] = []
        for block in self._blocks(lines):
            content = self._content_lines(block)
            if not content:
                continue
            url = next((match.group(0) for line in content if (match := URL_PATTERN.search(line))), None)
            tech_line = next((line for line in content[1:] if re.search(r"(?:tech(?:nologies)?|stack)\s*:", line, re.I)), "")
            technologies = re.split(r"[,;|]", tech_line.split(":", 1)[-1]) if tech_line else []
            projects.append(ResumeProject(name=content[0], url=url, technologies=self._deduplicate(technologies), description=content[1:]))
        return projects

    def extract_education(self, lines: list[str]) -> list[ResumeEducation]:
        """Parse education blocks into degree and institution fields."""
        entries: list[ResumeEducation] = []
        for block in self._blocks(lines):
            content = self._content_lines(block)
            if not content:
                continue
            first, second = content[0], content[1] if len(content) > 1 else None
            degree = first if self._looks_like_degree(first) else second
            institution = second if degree == first else first
            start, end = self._date_range(" ".join(content))
            entries.append(ResumeEducation(institution=institution, degree=degree, field_of_study=self._field_from_degree(degree), start_date=start, end_date=end, description=content[2:]))
        return entries

    def extract_certifications(self, lines: list[str]) -> list[ResumeCertification]:
        """Parse each listed certification, optionally recognizing issuer and date."""
        results: list[ResumeCertification] = []
        for line in self._content_lines(lines):
            parts = [part.strip() for part in re.split(r"\s+(?:[-|–—]|by)\s+", line, maxsplit=1, flags=re.I)]
            date = self._first_match(DATE_PATTERN, line)
            results.append(ResumeCertification(name=parts[0], issuer=parts[1] if len(parts) > 1 else None, date=date))
        return results

    def extract_languages(self, lines: list[str]) -> list[ResumeLanguage]:
        """Parse language entries in ``Language - proficiency`` form."""
        languages: list[ResumeLanguage] = []
        for line in self._content_lines(lines):
            for item in re.split(r"[,;|]", line):
                parts = re.split(r"\s*(?:[-–—:]|\()\s*", item.strip(), maxsplit=1)
                if parts and parts[0]:
                    proficiency = parts[1].rstrip(") ") if len(parts) > 1 else None
                    languages.append(ResumeLanguage(name=parts[0], proficiency=proficiency))
        return languages

    def _detect_sections(self, text: str) -> tuple[dict[str, list[str]], str]:
        sections: dict[str, list[str]] = {}
        preamble: list[str] = []
        current: str | None = None
        for line in text.splitlines():
            section = self._section_name(line)
            if section:
                current = section
                sections.setdefault(section, [])
            elif current is None:
                preamble.append(line)
            else:
                sections[current].append(line)
        return sections, "\n".join(preamble)

    @staticmethod
    def _section_name(line: str) -> str | None:
        candidate = line.strip().rstrip(":").strip().casefold()
        candidate = re.sub(r"\s+", " ", candidate)
        if len(candidate) > MAX_HEADING_LENGTH:
            return None
        return SECTION_ALIASES.get(candidate)

    @staticmethod
    def _normalize_text(text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n").strip()

    @staticmethod
    def _content_lines(lines: Iterable[str]) -> list[str]:
        return [line.strip().lstrip("".join(BULLET_PREFIXES)).strip() for line in lines if line.strip()]

    def _blocks(self, lines: list[str]) -> list[list[str]]:
        blocks: list[list[str]] = []
        current: list[str] = []
        for line in lines:
            if not line.strip():
                if current:
                    blocks.append(current)
                    current = []
            elif current and DATE_RANGE_PATTERN.search(line) and any(DATE_RANGE_PATTERN.search(item) for item in current):
                blocks.append(current)
                current = [line]
            else:
                current.append(line)
        if current:
            blocks.append(current)
        return blocks

    def _experience_from_block(self, block: list[str]) -> ResumeExperience:
        content = self._content_lines(block)
        start, end = self._date_range(" ".join(content))
        non_date = [line for line in content if not DATE_RANGE_PATTERN.search(line)]
        company = non_date[0] if non_date else None
        title = non_date[1] if len(non_date) > 1 else None
        return ResumeExperience(company=company, title=title, start_date=start, end_date=end, description=non_date[2:])

    @staticmethod
    def _date_range(text: str) -> tuple[str | None, str | None]:
        match = DATE_RANGE_PATTERN.search(text)
        return (match.group("start"), match.group("end")) if match else (None, None)

    @staticmethod
    def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
        match = pattern.search(text)
        return match.group(0) if match else None

    @staticmethod
    def _extract_name(lines: list[str], email: str | None, phone: str | None) -> str | None:
        for line in lines[:4]:
            candidate = line.strip()
            if not candidate or email and email in candidate or phone and phone in candidate or "@" in candidate or "://" in candidate:
                continue
            if re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,80}", candidate) and len(candidate.split()) >= 2:
                return candidate
        return None

    @staticmethod
    def _looks_like_degree(value: str) -> bool:
        return bool(re.search(r"\b(?:b\.?tech|b\.?sc|m\.?sc|bachelor|master|ph\.?d|mba|diploma|associate)\b", value, re.I))

    @staticmethod
    def _field_from_degree(degree: str | None) -> str | None:
        if not degree:
            return None
        match = re.search(r"(?:in|of)\s+(.+)$", degree, re.I)
        if match:
            return match.group(1).strip()
        abbreviated = re.match(r"(?:b|m)\.?\s*(?:tech|sc|s)\.?\s+(.+)$", degree, re.I)
        return abbreviated.group(1).strip() if abbreviated else None

    @staticmethod
    def _deduplicate(values: Iterable[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            cleaned = value.strip()
            key = cleaned.casefold()
            if cleaned and key not in seen:
                seen.add(key)
                result.append(cleaned)
        return result
