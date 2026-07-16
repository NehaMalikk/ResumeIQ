"""Tests for the reusable deterministic Skill Extraction Engine."""

from ai_engine.extraction.categories import categorize
from ai_engine.extraction.normalizer import SkillNormalizer
from ai_engine.extraction.skill_extractor import SkillExtractor


def test_extracts_normalizes_and_deduplicates_skills() -> None:
    text = "I have worked with Python, py, FastAPI, ReactJS, Docker, AWS Cloud, Postgres."
    assert SkillExtractor().extract(text) == ["Python", "FastAPI", "React", "Docker", "AWS", "PostgreSQL"]


def test_normalizes_synonyms_case_spacing_and_punctuation() -> None:
    normalizer = SkillNormalizer()
    assert normalizer.normalize("NODE js") == "Node.js"
    assert normalizer.normalize("github") == "GitHub"
    assert normalizer.normalize("scikit learn") == "Scikit-Learn"
    assert normalizer.normalize("unknown tool") is None


def test_categorizes_canonical_skills() -> None:
    assert categorize("Python") == "Programming Language"
    assert categorize("Docker") == "DevOps"
    assert categorize("AWS") == "Cloud"
    assert categorize("py") == "Programming Language"
    assert categorize("not a skill") is None


def test_prefers_longest_overlapping_skill_match() -> None:
    assert SkillExtractor().extract("GitHub Actions with GitHub and Git") == ["GitHub Actions", "GitHub", "Git"]


def test_handles_large_text_random_text_and_no_skills() -> None:
    extractor = SkillExtractor()
    large_resume = ("Built APIs with Python and Docker. " * 2_000) + "Used Kubernetes."
    assert extractor.extract(large_resume) == ["Python", "Docker", "Kubernetes"]
    assert extractor.extract("A stroll through the orchard at sunrise.") == []
    assert extractor.extract("") == []
