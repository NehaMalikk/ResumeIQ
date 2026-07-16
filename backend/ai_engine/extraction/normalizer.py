"""Canonicalization of known technical-skill names."""

from __future__ import annotations

import re

from ai_engine.extraction.skill_dictionary import SKILL_ALIASES, SKILL_CATEGORIES


class SkillNormalizer:
    """Normalize known aliases, casing, whitespace, and punctuation variants."""

    def __init__(self) -> None:
        self._lookup = {self._key(name): name for name in SKILL_CATEGORIES} | {self._key(alias): canonical for alias, canonical in SKILL_ALIASES.items()}

    def normalize(self, skill: str) -> str | None:
        """Return a canonical known skill, or ``None`` when it is not known."""
        return self._lookup.get(self._key(skill)) if isinstance(skill, str) else None

    @staticmethod
    def _key(value: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[._-]+", " ", value.strip().casefold()))
