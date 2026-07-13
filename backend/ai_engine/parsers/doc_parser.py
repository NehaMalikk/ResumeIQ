"""Word document parser for resume files.

This module will handle extraction of raw text from DOC and DOCX resume
uploads. Future responsibilities include:

- DOCX XML parsing with formatting preservation
- Legacy DOC format support
- Table and list structure extraction
- Header/footer removal
"""

from pathlib import Path


class DocParser:
    """Parse Word document resumes into structured raw text."""

    def parse(self, file_path: Path) -> str:
        """Extract raw text content from a Word document.

        Args:
            file_path: Absolute or relative path to the DOC/DOCX resume.

        Returns:
            Raw text extracted from the document.

        Raises:
            NotImplementedError: Parsing logic is not yet implemented.
        """
        # TODO: Support both .doc and .docx formats
        # TODO: Extract hyperlinks (LinkedIn, portfolio URLs)
        # TODO: Normalize bullet points and numbered lists
        raise NotImplementedError("Word document parsing is not yet implemented")
