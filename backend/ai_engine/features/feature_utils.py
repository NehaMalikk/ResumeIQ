"""Pure deterministic helpers shared by resume and JD feature builders."""

from __future__ import annotations

import math
import re
from collections.abc import Iterable


EDUCATION_RANKS = {"Unknown": 0, "High School": 1, "Diploma": 2, "Associate": 3, "Bachelor": 4, "Master": 5, "PhD": 6}


def education_level(text: str | None) -> str:
    """Map a degree string to the highest supported normalized level."""
    value = (text or "").casefold()
    if re.search(r"\b(?:ph\.?d|doctorate|doctoral)\b", value): return "PhD"
    if re.search(r"\b(?:master|m\.?sc|m\.?tech|mba)\b", value): return "Master"
    if re.search(r"\b(?:bachelor|b\.?sc|b\.?tech|b\.?e\.?|beng)\b", value): return "Bachelor"
    if "associate" in value: return "Associate"
    if re.search(r"\b(?:diploma|certificate)\b", value): return "Diploma"
    if re.search(r"\b(?:high school|secondary|higher secondary)\b", value): return "High School"
    return "Unknown"


def highest_education(values: Iterable[str | None]) -> str:
    return max((education_level(value) for value in values), key=EDUCATION_RANKS.__getitem__, default="Unknown")


def parse_experience_years(text: str | None) -> float | None:
    """Return the lower bound of a stated years-of-experience requirement."""
    if not text: return None
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|–|—|to)?\s*(?:\d+(?:\.\d+)?)?\+?\s*(?:years?|yrs?)", text, re.I)
    return float(match.group(1)) if match else None


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w+#.]+\b", text))


def estimate_pages(words: int, words_per_page: int = 500) -> int:
    return max(1, math.ceil(words / words_per_page)) if words else 0


def section_completeness(present: int, total: int) -> float:
    return round(present / total, 2) if total else 0.0


def technical_strength(skill_count: int, category_count: int, projects: int, experience_years: float | None, certifications: int) -> float:
    """Return a transparent 0..1 strength indicator; it is not an ATS score."""
    score = min(skill_count, 12) / 12 * 0.35
    score += min(category_count, 6) / 6 * 0.20
    score += min(projects, 4) / 4 * 0.20
    score += min(experience_years or 0, 8) / 8 * 0.15
    score += min(certifications, 4) / 4 * 0.10
    return round(min(score, 1.0), 2)
