"""Tests for ImageParser."""

from unittest.mock import patch

import pytest
from PIL import Image, ImageDraw

from ai_engine.parsers.exceptions import DocumentParsingError, OCRFailure
from ai_engine.parsers.image_parser import ImageParser


def test_extract_text_from_valid_image(sample_png) -> None:
    parser = ImageParser()

    with patch(
        "ai_engine.parsers.image_parser.pytesseract.image_to_string",
        return_value="OCR Sample Text",
    ):
        text = parser.extract_text(str(sample_png))

    assert text == "OCR Sample Text"


def test_extract_text_supports_jpg_and_jpeg(tmp_path) -> None:
    parser = ImageParser()

    for extension in (".jpg", ".jpeg"):
        path = tmp_path / f"resume{extension}"
        image = Image.new("RGB", (240, 80), color="white")
        draw = ImageDraw.Draw(image)
        draw.text((10, 20), "JPEG OCR Text", fill="black")
        image.save(path, format="JPEG")

        with patch(
            "ai_engine.parsers.image_parser.pytesseract.image_to_string",
            return_value="JPEG OCR Text",
        ):
            assert parser.extract_text(str(path)) == "JPEG OCR Text"


def test_extract_text_raises_for_missing_file(tmp_path) -> None:
    parser = ImageParser()
    missing = tmp_path / "missing.png"

    with pytest.raises(DocumentParsingError, match="File not found"):
        parser.extract_text(str(missing))


def test_extract_text_raises_for_unsupported_format(tmp_path) -> None:
    parser = ImageParser()
    path = tmp_path / "image.gif"
    Image.new("RGB", (50, 50), color="white").save(path, format="GIF")

    with pytest.raises(DocumentParsingError, match="Unsupported image format"):
        parser.extract_text(str(path))


def test_extract_text_raises_for_blank_image(blank_png) -> None:
    parser = ImageParser()

    with pytest.raises(OCRFailure, match="blank"):
        parser.extract_text(str(blank_png))


def test_extract_text_raises_when_ocr_returns_empty(sample_png) -> None:
    parser = ImageParser()

    with patch(
        "ai_engine.parsers.image_parser.pytesseract.image_to_string",
        return_value="   ",
    ):
        with pytest.raises(OCRFailure, match="did not detect any text"):
            parser.extract_text(str(sample_png))


def test_extract_text_raises_for_unreadable_image(tmp_path) -> None:
    parser = ImageParser()
    path = tmp_path / "broken.png"
    path.write_bytes(b"not-an-image")

    with pytest.raises(OCRFailure, match="corrupted or unreadable"):
        parser.extract_text(str(path))
