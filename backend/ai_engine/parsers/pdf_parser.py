"""PDF document parser."""

from pathlib import Path

import pdfplumber
from pdfminer.pdfdocument import PDFEncryptionError, PDFPasswordIncorrect

from ai_engine.parsers.exceptions import DocumentParsingError
from app.core.logging import get_logger

logger = get_logger(__name__)


class PDFParser:
    """Extract plain text from PDF documents."""

    def extract_text(self, file_path: str) -> str:
        """Extract all text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            UTF-8 plain text with line breaks preserved where appropriate.

        Raises:
            DocumentParsingError: If the file is missing, encrypted, empty,
                corrupted, or otherwise unreadable.
        """
        path = Path(file_path)
        file_name = path.name

        if not path.is_file():
            logger.error("PDF extraction failed: invalid path '%s'", file_path)
            raise DocumentParsingError(
                f"File not found or not a regular file: {file_path}",
                file_name=file_name,
            )

        logger.info("Starting PDF extraction for '%s'", file_name)

        try:
            with pdfplumber.open(path) as pdf:
                pages_text: list[str] = []
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    pages_text.append(page_text.rstrip())

                text = "\n\n".join(pages_text).strip()
        except DocumentParsingError:
            raise
        except (PDFPasswordIncorrect, PDFEncryptionError) as exc:
            logger.exception("PDF extraction failed: encrypted PDF '%s'", file_name)
            raise DocumentParsingError(
                "PDF is encrypted and cannot be read without a password.",
                file_name=file_name,
            ) from exc
        except Exception as exc:
            logger.exception("PDF extraction failed: corrupted PDF '%s'", file_name)
            raise DocumentParsingError(
                f"Failed to parse PDF: {exc}",
                file_name=file_name,
            ) from exc

        if not text:
            logger.error("PDF extraction failed: empty PDF '%s'", file_name)
            raise DocumentParsingError(
                "PDF contains no extractable text.",
                file_name=file_name,
            )

        logger.info("PDF extraction succeeded for '%s' (%d characters)", file_name, len(text))
        return text
