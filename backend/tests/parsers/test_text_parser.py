"""Tests for TextParser."""

import pytest

from ai_engine.parsers.exceptions import DocumentParsingError
from ai_engine.parsers.text_parser import TextParser


def test_extract_text_normalizes_whitespace_and_newlines() -> None:
    parser = TextParser()
    raw = "  Senior   Engineer  \r\n\r\n\r\nPython   FastAPI  \n"

    cleaned = parser.extract_text(raw)

    assert cleaned == "Senior Engineer\n\nPython FastAPI"


def test_extract_text_strips_outer_whitespace() -> None:
    parser = TextParser()

    assert parser.extract_text("   hello world   ") == "hello world"


def test_extract_text_returns_empty_string_for_blank_input() -> None:
    parser = TextParser()

    assert parser.extract_text("   \n\t  ") == ""


def test_extract_text_rejects_non_string_input() -> None:
    parser = TextParser()

    with pytest.raises(DocumentParsingError, match="must be a string"):
        parser.extract_text(None)  # type: ignore[arg-type]
