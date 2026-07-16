"""Compiled regular expressions used by the job-description parser."""

from __future__ import annotations

import re


EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
URL_PATTERN = re.compile(r"(?:https?://|www\.)[^\s,;|]+", re.IGNORECASE)
EXPERIENCE_PATTERN = re.compile(
    r"\b(?:minimum\s+of\s+|at\s+least\s+|over\s+)?\d+(?:\s*[-–—to]+\s*\d+)?\+?\s*(?:years?|yrs?)\b(?:\s+(?:of|in)\s+[A-Za-z][A-Za-z /&-]{0,60})?",
    re.IGNORECASE,
)
SALARY_PATTERN = re.compile(
    r"(?:[$€£₹]\s?\d[\d,]*(?:\.\d{1,2})?(?:\s?[kKmM])?|\b\d[\d,]*(?:\.\d{1,2})?\s?(?:USD|EUR|GBP|INR))"
    r"(?:\s*(?:-|–|—|to)\s*(?:[$€£₹]\s?\d[\d,]*(?:\.\d{1,2})?(?:\s?[kKmM])?|\d[\d,]*(?:\.\d{1,2})?\s?(?:USD|EUR|GBP|INR)))?"
    r"(?:\s*(?:/\s*(?:year|yr|month|hour)|per\s+(?:year|annum|hour)))?",
    re.IGNORECASE,
)
KEYWORD_PHRASE_PATTERN = re.compile(r"\b(?:REST APIs?|microservices?|CI/CD|agile|scrum|machine learning|deep learning|cloud computing|data pipelines?)\b", re.IGNORECASE)
