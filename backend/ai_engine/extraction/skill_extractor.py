"""Deterministic extraction of normalized technical skills from plain text."""

from __future__ import annotations

import logging
import re

from ai_engine.extraction.normalizer import SkillNormalizer
from ai_engine.extraction.skill_dictionary import SKILL_ALIASES, SKILL_CATEGORIES

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extract known technical skills without semantic, AI, or ML matching."""

    def __init__(self, normalizer: SkillNormalizer | None = None) -> None:
        self._normalizer = normalizer or SkillNormalizer()
        alternatives = "|".join(re.escape(term) for term in sorted([*SKILL_CATEGORIES, *SKILL_ALIASES], key=len, reverse=True))
        # A period may be ordinary sentence punctuation after a skill (for
        # example, ``Postgres.``), so it must not block the final boundary.
        self._pattern = re.compile(rf"(?<![A-Za-z0-9+#.])(?:{alternatives})(?![A-Za-z0-9+#])", re.IGNORECASE)

    def extract(self, text: str) -> list[str]:
        """Return unique canonical skills in their first-occurrence order."""
        logger.info("Skill extraction started")
        if not isinstance(text, str) or not text.strip():
            logger.info("Skills detected: none")
            logger.info("Skill extraction complete")
            return []
        detected: list[str] = []
        seen: set[str] = set()
        for match in self._pattern.finditer(text):
            canonical = self._normalizer.normalize(match.group())
            if canonical and canonical not in seen:
                seen.add(canonical)
                detected.append(canonical)
        logger.info("Skills detected: %s", ", ".join(detected) or "none")
        logger.info("Normalization complete")
        logger.info("Skill extraction complete")
        return detected
