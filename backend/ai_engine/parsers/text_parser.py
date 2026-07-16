"""Plain text normalization parser."""

import re

from ai_engine.parsers.exceptions import DocumentParsingError
from app.core.logging import get_logger

logger = get_logger(__name__)


class TextParser:
    """Normalize and clean plain UTF-8 text input."""

    def extract_text(self, text: str) -> str:
        """Strip unnecessary whitespace and normalize newlines.

        Args:
            text: Raw plain text content.

        Returns:
            Cleaned UTF-8 string.
        """
        if not isinstance(text, str):
            logger.error(
                "Plain text normalization failed: expected str, received %s",
                type(text).__name__,
            )
            raise DocumentParsingError("Plain text input must be a string.")

        logger.debug(
            "Starting plain text normalization with TextParser (%d characters)",
            len(text),
        )

        normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in normalized.split("\n")]
        collapsed = "\n".join(lines)
        cleaned = re.sub(r"\n{3,}", "\n\n", collapsed).strip()

        logger.info(
            "Plain text normalization succeeded with TextParser (%d characters)",
            len(cleaned),
        )
        return cleaned
