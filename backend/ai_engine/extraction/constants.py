"""Constants used by the deterministic resume structure parser."""

from __future__ import annotations

from collections.abc import Mapping


SECTION_ALIASES: Mapping[str, str] = {
    "summary": "summary",
    "professional summary": "summary",
    "career summary": "summary",
    "profile": "summary",
    "objective": "summary",
    "career objective": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "core competencies": "skills",
    "competencies": "skills",
    "technologies": "skills",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "employment": "experience",
    "employment history": "experience",
    "work history": "experience",
    "volunteer experience": "experience",
    "projects": "projects",
    "academic projects": "projects",
    "personal projects": "projects",
    "project experience": "projects",
    "education": "education",
    "academic qualifications": "education",
    "qualifications": "education",
    "certifications": "certifications",
    "certificates": "certifications",
    "licenses and certifications": "certifications",
    "achievements": "certifications",
    "languages": "languages",
}

SECTION_NAMES = frozenset(SECTION_ALIASES.values())

# Headings are normally short; imposing a limit prevents prose from being
# mistakenly treated as a section just because it contains a known phrase.
MAX_HEADING_LENGTH = 60

BULLET_PREFIXES = ("-", "*", "•", "‣", "▪", "◦")
