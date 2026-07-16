"""Parser factory for automatic document type detection."""

import os
from pathlib import Path
from typing import Protocol, TypeAlias

from ai_engine.parsers.doc_parser import DocumentParser
from ai_engine.parsers.exceptions import InvalidFileType
from ai_engine.parsers.image_parser import ImageParser
from ai_engine.parsers.pdf_parser import PDFParser
from ai_engine.parsers.text_parser import TextParser
from app.core.logging import get_logger

logger = get_logger(__name__)


class HasFilename(Protocol):
    """Structural type for upload objects exposing an original filename."""

    filename: str | None


FileInput: TypeAlias = str | os.PathLike[str] | HasFilename

_PARSER_MAP: dict[str, type] = {
    ".pdf": PDFParser,
    ".doc": DocumentParser,
    ".docx": DocumentParser,
    ".png": ImageParser,
    ".jpg": ImageParser,
    ".jpeg": ImageParser,
    ".txt": TextParser,
}


class ParserFactory:
    """Return the appropriate parser for an uploaded file."""

    @staticmethod
    def get_parser(file: FileInput) -> PDFParser | DocumentParser | ImageParser | TextParser:
        """Detect the file type and return a matching parser instance.

        Args:
            file: File path, path-like object, or upload object with a ``filename``.

        Returns:
            Parser instance for the detected file extension.

        Raises:
            InvalidFileType: If the extension is not supported.
        """
        file_name = ParserFactory._get_file_name(file)
        extension = Path(file_name).suffix.lower()

        parser_class = _PARSER_MAP.get(extension)
        if parser_class is None:
            logger.error(
                "Parser selection failed: unsupported file type '%s' for '%s'",
                extension or "(none)",
                file_name,
            )
            raise InvalidFileType(
                f"Unsupported file type: {extension or 'unknown'}",
                file_name=file_name,
            )

        parser = parser_class()
        logger.info(
            "Selected parser '%s' for file '%s'",
            parser_class.__name__,
            file_name,
        )
        return parser

    @staticmethod
    def _get_file_name(file: FileInput) -> str:
        """Return a filename without requiring the file to exist on disk."""
        if isinstance(file, (str, os.PathLike)):
            return Path(file).name

        file_name = getattr(file, "filename", None)
        if isinstance(file_name, str) and file_name:
            return Path(file_name).name

        logger.error("Parser selection failed: file has no usable filename")
        raise InvalidFileType("Unsupported file type: unknown")
