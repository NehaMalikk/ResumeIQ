"""Image-based resume parser using OCR.

This module will handle text extraction from image resume uploads (PNG, JPG,
TIFF). Future responsibilities include:

- OCR engine integration (Tesseract, EasyOCR, or cloud OCR APIs)
- Image preprocessing (deskew, denoise, contrast enhancement)
- Multi-language OCR support
- Confidence scoring per extracted text block
"""

from pathlib import Path


class ImageParser:
    """Parse image-based resumes using optical character recognition."""

    def parse(self, file_path: Path) -> str:
        """Extract raw text content from an image resume via OCR.

        Args:
            file_path: Absolute or relative path to the image file.

        Returns:
            Raw text extracted via OCR.

        Raises:
            NotImplementedError: OCR logic is not yet implemented.
        """
        # TODO: Preprocess image before OCR (grayscale, threshold, deskew)
        # TODO: Select OCR engine based on configuration
        # TODO: Post-process OCR output to fix common recognition errors
        raise NotImplementedError("Image OCR parsing is not yet implemented")
