"""Word document parser for DOC and DOCX files."""

from pathlib import Path
from zipfile import BadZipFile

from docx import Document
from docx.opc.exceptions import PackageNotFoundError

from ai_engine.parsers.exceptions import DocumentParsingError
from app.core.logging import get_logger

logger = get_logger(__name__)


class DocumentParser:
    """Extract plain text from Word documents (.doc and .docx)."""

    def extract_text(self, file_path: str) -> str:
        """Extract all paragraph text from a Word document.

        Args:
            file_path: Path to the DOC or DOCX file.

        Returns:
            UTF-8 plain text with paragraph line breaks preserved.

        Raises:
            DocumentParsingError: If the file is missing, empty, corrupted,
                or uses an unsupported legacy format.
        """
        path = Path(file_path)
        file_name = path.name
        extension = path.suffix.lower()

        if not path.is_file():
            logger.error("Document extraction failed: invalid path '%s'", file_path)
            raise DocumentParsingError(
                f"File not found or not a regular file: {file_path}",
                file_name=file_name,
            )

        logger.info("Starting document extraction for '%s'", file_name)

        if extension == ".doc":
            text = self._extract_legacy_doc(path, file_name)
        elif extension == ".docx":
            text = self._extract_docx(path, file_name)
        else:
            logger.error(
                "Document extraction failed: unsupported extension '%s' for '%s'",
                extension or "(none)",
                file_name,
            )
            raise DocumentParsingError(
                f"Unsupported Word document extension: {extension}",
                file_name=file_name,
            )

        if not text.strip():
            logger.error("Document extraction failed: empty document '%s'", file_name)
            raise DocumentParsingError(
                "Document contains no extractable text.",
                file_name=file_name,
            )

        logger.info(
            "Document extraction succeeded for '%s' (%d characters)",
            file_name,
            len(text),
        )
        return text

    def _extract_docx(self, path: Path, file_name: str) -> str:
        try:
            document = Document(path)
        except PackageNotFoundError as exc:
            logger.exception("Document extraction failed: invalid DOCX '%s'", file_name)
            raise DocumentParsingError(
                "Invalid or corrupted DOCX file.",
                file_name=file_name,
            ) from exc
        except (BadZipFile, OSError, ValueError, KeyError) as exc:
            logger.exception("Document extraction failed: corrupted DOCX '%s'", file_name)
            raise DocumentParsingError(
                "Invalid or corrupted DOCX file.",
                file_name=file_name,
            ) from exc

        # Retain paragraph boundaries, including intentional blank paragraphs.
        # ``str.strip`` belongs at the document boundary so internal line breaks
        # and spacing remain available to downstream consumers.
        return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()

    def _extract_legacy_doc(self, path: Path, file_name: str) -> str:
        """Extract text from legacy binary .doc files.

        Legacy .doc files are not supported by python-docx. This method performs
        a best-effort UTF-16-LE decode of readable content from the binary stream.
        """
        try:
            content = path.read_bytes()
        except OSError as exc:
            logger.exception("Document extraction failed: unreadable DOC '%s'", file_name)
            raise DocumentParsingError(
                f"Failed to read DOC file: {exc}",
                file_name=file_name,
            ) from exc

        if not content:
            raise DocumentParsingError(
                "Document contains no extractable text.",
                file_name=file_name,
            )

        try:
            decoded = content.decode("utf-16-le", errors="ignore")
        except Exception as exc:
            logger.exception("Document extraction failed: corrupted DOC '%s'", file_name)
            raise DocumentParsingError(
                f"Failed to parse legacy DOC file: {exc}",
                file_name=file_name,
            ) from exc

        lines: list[str] = []
        for raw_line in decoded.splitlines():
            cleaned = "".join(
                char for char in raw_line if char.isprintable() or char in {"\t"}
            ).strip()
            if cleaned:
                lines.append(cleaned)

        text = "\n".join(lines)
        if not text.strip():
            logger.error(
                "Document extraction failed: legacy DOC '%s' could not be decoded",
                file_name,
            )
            raise DocumentParsingError(
                "Legacy DOC file could not be parsed. Convert to DOCX or PDF.",
                file_name=file_name,
            )

        return text
