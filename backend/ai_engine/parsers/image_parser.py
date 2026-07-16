"""Image document parser using OCR."""

from pathlib import Path

import pytesseract
from PIL import Image, UnidentifiedImageError

from ai_engine.parsers.exceptions import DocumentParsingError, OCRFailure
from app.core.logging import get_logger

logger = get_logger(__name__)

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


class ImageParser:
    """Extract plain text from image documents via OCR."""

    def extract_text(self, file_path: str) -> str:
        """Run OCR on an image file and return extracted text.

        Args:
            file_path: Path to a PNG, JPG, or JPEG image.

        Returns:
            UTF-8 plain text extracted via OCR.

        Raises:
            DocumentParsingError: If the file path is invalid or the format
                is unsupported.
            OCRFailure: If the image is unreadable, blank, or OCR fails.
        """
        path = Path(file_path)
        file_name = path.name
        extension = path.suffix.lower()

        if not path.is_file():
            logger.error("Image OCR failed: invalid path '%s'", file_path)
            raise DocumentParsingError(
                f"File not found or not a regular file: {file_path}",
                file_name=file_name,
            )

        if extension not in SUPPORTED_IMAGE_EXTENSIONS:
            logger.error(
                "Image OCR failed: unsupported format '%s' for '%s'",
                extension,
                file_name,
            )
            raise DocumentParsingError(
                f"Unsupported image format: {extension}",
                file_name=file_name,
            )

        logger.info("Starting OCR extraction for '%s'", file_name)

        try:
            with Image.open(path) as image:
                image.load()
                if self._is_blank_image(image):
                    logger.error("Image OCR failed: blank image '%s'", file_name)
                    raise OCRFailure(
                        "Image appears blank and contains no readable text.",
                        file_name=file_name,
                    )

                text = pytesseract.image_to_string(image).strip()
        except OCRFailure:
            raise
        except UnidentifiedImageError as exc:
            logger.exception("Image OCR failed: unreadable image '%s'", file_name)
            raise OCRFailure(
                "Image file is corrupted or unreadable.",
                file_name=file_name,
            ) from exc
        except pytesseract.TesseractNotFoundError as exc:
            logger.exception("Image OCR failed: Tesseract not installed")
            raise OCRFailure(
                "Tesseract OCR engine is not installed or not on PATH.",
                file_name=file_name,
            ) from exc
        except Exception as exc:
            logger.exception("Image OCR failed for '%s'", file_name)
            raise OCRFailure(
                f"OCR extraction failed: {exc}",
                file_name=file_name,
            ) from exc

        if not text:
            logger.error("Image OCR failed: no text detected in '%s'", file_name)
            raise OCRFailure(
                "OCR did not detect any text in the image.",
                file_name=file_name,
            )

        logger.info("OCR extraction succeeded for '%s' (%d characters)", file_name, len(text))
        return text

    @staticmethod
    def _is_blank_image(image: Image.Image) -> bool:
        """Return True when every pixel is effectively blank."""
        grayscale = image.convert("L")
        extrema = grayscale.getextrema()
        if extrema is None:
            return True
        minimum, maximum = extrema
        return maximum - minimum <= 1
