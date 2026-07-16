"""Section aliases and small vocabulary constants for job descriptions."""

from __future__ import annotations

from collections.abc import Mapping


JD_SECTION_ALIASES: Mapping[str, str] = {
    "job title": "title", "title": "title", "position": "title", "role": "title",
    "company": "company", "company name": "company", "about us": "about", "who we are": "about",
    "about the role": "about", "about the job": "about", "job overview": "about",
    "responsibilities": "responsibilities", "key responsibilities": "responsibilities", "what you'll do": "responsibilities",
    "requirements": "requirements", "job requirements": "requirements", "what we're looking for": "requirements",
    "required skills": "required_skills", "must have skills": "required_skills", "must-have skills": "required_skills",
    "preferred skills": "preferred_skills", "preferred qualifications": "preferred_skills",
    "nice to have": "nice_to_have_skills", "nice-to-have": "nice_to_have_skills", "bonus skills": "nice_to_have_skills",
    "qualifications": "qualifications", "minimum qualifications": "qualifications",
    "education": "education", "education requirements": "education",
    "experience": "experience", "experience required": "experience",
    "benefits": "benefits", "perks": "benefits", "what we offer": "benefits",
    "certifications": "certifications", "licenses": "certifications",
    "salary": "salary", "compensation": "salary", "pay range": "salary",
    "location": "location", "job location": "location", "work location": "location",
    "employment type": "employment_type", "job type": "employment_type", "work type": "employment_type",
    "department": "department", "team": "department",
}

JD_SECTION_NAMES = frozenset(JD_SECTION_ALIASES.values())
MAX_JD_HEADING_LENGTH = 80
BULLET_PREFIXES = ("-", "*", "•", "‣", "▪", "◦", "–", "—")
EMPLOYMENT_TYPES = ("full-time", "part-time", "contract", "temporary", "internship", "freelance", "permanent")
