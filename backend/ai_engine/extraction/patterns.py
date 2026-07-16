"""Compiled regular expressions for resume structure extraction."""

from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(
    r"(?<!\w)(?:\+?\d{1,3}[.\s-]?)?(?:\(?\d{2,4}\)?[.\s-]?)?\d{3,4}[.\s-]\d{3,4}(?!\w)"
)
URL_PATTERN = re.compile(r"(?:https?://|www\.)[^\s,;|]+", re.IGNORECASE)
LINKEDIN_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[^\s,;|]+", re.IGNORECASE)
GITHUB_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[^\s,;|]+", re.IGNORECASE)
DATE_PATTERN = re.compile(
    r"(?:"
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|"
    r"aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)[\s,.-]*\d{4}"
    r"|\d{1,2}[/-]\d{4}|\d{4}"
    r")",
    re.IGNORECASE,
)
DATE_RANGE_PATTERN = re.compile(
    rf"(?P<start>{DATE_PATTERN.pattern})\s*(?:-|–|—|to)\s*(?P<end>{DATE_PATTERN.pattern}|present|current|now)",
    re.IGNORECASE,
)
YEAR_PATTERN = re.compile(r"\b(?:19|20)\d{2}\b")
