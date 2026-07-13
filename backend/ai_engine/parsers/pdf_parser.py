"""PDF document parser for resume files.

This module will handle extraction of raw text and layout metadata from
PDF resume uploads. Future responsibilities include:

- Multi-page PDF text extraction
- Layout-aware parsing (columns, sections, headers)
- Handling of embedded fonts and scanned PDF detection
- Metadata extraction (author, creation date)
"""

from pathlib import Path


class PDFParser:
    """Parse PDF resume documents into structured raw text."""

    def parse(self, file_path: Path) -> str:
        """Extract raw text content from a PDF file.

        Args:
            file_path: Absolute or relative path to the PDF resume.

        Returns:
            Raw text extracted from the document.

        Raises:
            NotImplementedError: Parsing logic is not yet implemented.
        """
        # TODO: Integrate a PDF extraction library (e.g., PyMuPDF, pdfplumber)
        # TODO: Detect scanned vs. native PDFs and route to OCR if needed
        # TODO: Preserve section boundaries for downstream NLP
        raise NotImplementedError("PDF parsing is not yet implemented")
