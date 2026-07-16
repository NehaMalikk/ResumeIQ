"""Tests for PDFParser."""

from unittest.mock import patch

import pytest
from pdfminer.pdfdocument import PDFPasswordIncorrect

from ai_engine.parsers.exceptions import DocumentParsingError
from ai_engine.parsers.pdf_parser import PDFParser


def test_extract_text_from_valid_pdf(sample_pdf) -> None:
    parser = PDFParser()
    text = parser.extract_text(str(sample_pdf))

    assert "Jane Doe" in text
    assert "Software Engineer" in text


def test_extract_text_raises_for_missing_file(tmp_path) -> None:
    parser = PDFParser()
    missing = tmp_path / "missing.pdf"

    with pytest.raises(DocumentParsingError, match="File not found"):
        parser.extract_text(str(missing))


def test_extract_text_raises_for_empty_pdf(empty_pdf) -> None:
    parser = PDFParser()

    with pytest.raises(DocumentParsingError, match="no extractable text"):
        parser.extract_text(str(empty_pdf))


def test_extract_text_raises_for_corrupted_pdf(corrupted_pdf) -> None:
    parser = PDFParser()

    with pytest.raises(DocumentParsingError, match="Failed to parse PDF"):
        parser.extract_text(str(corrupted_pdf))


def test_extract_text_raises_for_encrypted_pdf(sample_pdf) -> None:
    parser = PDFParser()

    with patch(
        "ai_engine.parsers.pdf_parser.pdfplumber.open",
        side_effect=PDFPasswordIncorrect,
    ):
        with pytest.raises(DocumentParsingError, match="encrypted"):
            parser.extract_text(str(sample_pdf))
