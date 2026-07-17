"""Coverage for the deterministic ATS score adapter."""
from __future__ import annotations

from types import SimpleNamespace

from ai_engine.comparison import ComparisonMetric, ComparisonResult
from ai_engine.scoring import ATSScoringEngine, ScoringWeights


def _result(score: float, confidence: float = 1.0) -> ComparisonResult:
    names = ("skills", "experience", "education", "projects", "certifications", "keywords", "responsibilities", "semantic")
    return ComparisonResult(
        overall_score=score,
        metrics=[ComparisonMetric(name=name, score=score, confidence=confidence) for name in names],
    )


def test_perfect_partial_and_no_match_scores() -> None:
    engine = ATSScoringEngine()
    assert engine.score(_result(100)).overall_score == 100
    assert engine.score(_result(50)).overall_score == 50
    assert engine.score(_result(0)).overall_score == 0


def test_empty_and_missing_outputs_are_safe() -> None:
    empty = ATSScoringEngine().score(ComparisonResult(overall_score=0))
    missing = ATSScoringEngine().score(SimpleNamespace(metrics=[{"name": "skills", "score": 80, "confidence": 1}]))
    assert empty.overall_score == 0 and empty.confidence == 0
    assert missing.skills_score == 80 and missing.overall_score == 24
    assert any("Missing comparison output" in warning for warning in missing.warnings)


def test_invalid_weights_and_metrics_are_validated() -> None:
    engine = ATSScoringEngine(ScoringWeights(values={"skills": -1, "experience": "bad"}))  # type: ignore[dict-item]
    score = engine.score({"metrics": [{"name": "skills", "score": -50, "confidence": 2}]})
    assert 0 <= score.overall_score <= 100
    assert any("weight" in warning.lower() for warning in score.warnings)


def test_confidence_and_breakdown() -> None:
    complete = ATSScoringEngine().score(_result(80, confidence=1))
    incomplete = ATSScoringEngine().score({"metrics": [{"name": "skills", "score": 80, "confidence": 0.5}]})
    assert complete.confidence == 1
    assert 0 < incomplete.confidence < complete.confidence
    for category in ("Skills", "Experience", "Education", "Projects", "Certifications", "Keywords", "Responsibilities", "Semantic"):
        assert category in incomplete.score_breakdown.explanation


def test_score_is_clamped_for_malformed_duck_typed_metrics() -> None:
    result = {"metrics": [{"name": "skills", "score": 500, "confidence": 4}, {"name": "experience", "score": -4, "confidence": -2}]}
    score = ATSScoringEngine().score(result)
    assert score.skills_score == 100
    assert score.experience_score == 0
    assert 0 <= score.overall_score <= 100
