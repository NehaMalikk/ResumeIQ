"""Custom exceptions for document parsing."""


class DocumentParsingError(Exception):
    """Raised when a document cannot be parsed."""

    def __init__(self, message: str, *, file_name: str | None = None) -> None:
        self.file_name = file_name
        super().__init__(message)


class InvalidFileType(DocumentParsingError):
    """Raised when an uploaded file has an unsupported extension."""


class OCRFailure(DocumentParsingError):
    """Raised when OCR text extraction fails."""
