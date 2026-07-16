"""Tests for DocumentParser."""

import pytest
from docx import Document

from ai_engine.parsers.doc_parser import DocumentParser
from ai_engine.parsers.exceptions import DocumentParsingError


def test_extract_text_from_valid_docx(sample_docx) -> None:
    parser = DocumentParser()
    text = parser.extract_text(str(sample_docx))

    assert "Jane Doe" in text
    assert "Backend Developer" in text
    assert "\n" in text


def test_extract_text_from_legacy_doc(legacy_doc) -> None:
    parser = DocumentParser()
    text = parser.extract_text(str(legacy_doc))

    assert "Legacy Resume Content" in text


def test_extract_text_raises_for_missing_file(tmp_path) -> None:
    parser = DocumentParser()
    missing = tmp_path / "missing.docx"

    with pytest.raises(DocumentParsingError, match="File not found"):
        parser.extract_text(str(missing))


def test_extract_text_raises_for_empty_docx(empty_docx) -> None:
    parser = DocumentParser()

    with pytest.raises(DocumentParsingError, match="no extractable text"):
        parser.extract_text(str(empty_docx))


def test_extract_text_raises_for_corrupted_docx(tmp_path) -> None:
    parser = DocumentParser()
    path = tmp_path / "broken.docx"
    path.write_bytes(b"not-a-docx")

    with pytest.raises(DocumentParsingError, match="Invalid or corrupted DOCX"):
        parser.extract_text(str(path))


def test_extract_text_raises_for_empty_legacy_doc(tmp_path) -> None:
    parser = DocumentParser()
    path = tmp_path / "empty.doc"
    path.write_bytes(b"\x00" * 32)

    with pytest.raises(DocumentParsingError):
        parser.extract_text(str(path))
