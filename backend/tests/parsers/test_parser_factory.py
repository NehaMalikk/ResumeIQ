"""Tests for ParserFactory."""

from pathlib import Path

import pytest

from ai_engine.parsers.doc_parser import DocumentParser
from ai_engine.parsers.exceptions import InvalidFileType
from ai_engine.parsers.image_parser import ImageParser
from ai_engine.parsers.parser_factory import ParserFactory
from ai_engine.parsers.pdf_parser import PDFParser
from ai_engine.parsers.text_parser import TextParser


@pytest.mark.parametrize(
    ("file_name", "expected_parser"),
    [
        ("resume.pdf", PDFParser),
        ("resume.doc", DocumentParser),
        ("resume.docx", DocumentParser),
        ("scan.png", ImageParser),
        ("scan.jpg", ImageParser),
        ("scan.jpeg", ImageParser),
        ("job.txt", TextParser),
    ],
)
def test_get_parser_returns_expected_parser(file_name: str, expected_parser: type) -> None:
    parser = ParserFactory.get_parser(file_name)

    assert isinstance(parser, expected_parser)


def test_get_parser_is_case_insensitive() -> None:
    parser = ParserFactory.get_parser("Resume.PDF")

    assert isinstance(parser, PDFParser)


def test_get_parser_accepts_path_object() -> None:
    parser = ParserFactory.get_parser(Path("resume.docx"))

    assert isinstance(parser, DocumentParser)


def test_get_parser_accepts_upload_like_object() -> None:
    class Upload:
        filename = "candidate.JPEG"

    assert isinstance(ParserFactory.get_parser(Upload()), ImageParser)


def test_get_parser_rejects_upload_without_filename() -> None:
    class Upload:
        filename = None

    with pytest.raises(InvalidFileType, match="Unsupported file type"):
        ParserFactory.get_parser(Upload())


def test_get_parser_raises_for_unsupported_type(unsupported_file) -> None:
    with pytest.raises(InvalidFileType, match="Unsupported file type"):
        ParserFactory.get_parser(str(unsupported_file))


def test_get_parser_raises_for_missing_extension() -> None:
    with pytest.raises(InvalidFileType, match="Unsupported file type"):
        ParserFactory.get_parser("resume")


def test_end_to_end_file_extraction(sample_pdf, sample_docx, sample_txt, sample_png) -> None:
    """Factory-selected parsers produce plain text from supported files."""
    from unittest.mock import patch

    pdf_text = PDFParser().extract_text(str(sample_pdf))
    assert "Jane Doe" in pdf_text

    docx_text = DocumentParser().extract_text(str(sample_docx))
    assert "Jane Doe" in docx_text

    txt_parser = ParserFactory.get_parser(str(sample_txt))
    assert isinstance(txt_parser, TextParser)
    txt_text = txt_parser.extract_text(sample_txt.read_text(encoding="utf-8"))
    assert "Senior Engineer" in txt_text

    with patch(
        "ai_engine.parsers.image_parser.pytesseract.image_to_string",
        return_value="OCR Sample Text",
    ):
        png_text = ImageParser().extract_text(str(sample_png))
    assert png_text == "OCR Sample Text"
