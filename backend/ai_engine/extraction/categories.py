"""Skill category lookup."""

from __future__ import annotations

from ai_engine.extraction.skill_dictionary import SKILL_CATEGORIES
from ai_engine.extraction.normalizer import SkillNormalizer

_NORMALIZER = SkillNormalizer()


def categorize(skill: str) -> str | None:
    """Return the category of a known skill or one of its supported aliases."""
    canonical = _NORMALIZER.normalize(skill)
    return SKILL_CATEGORIES.get(canonical) if canonical else None
