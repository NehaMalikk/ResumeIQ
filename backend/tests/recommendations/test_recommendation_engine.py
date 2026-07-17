from __future__ import annotations

from dataclasses import replace

import pytest

from ai_engine.comparison.comparison_models import ComparisonMetric, ComparisonResult
from ai_engine.recommendations import RecommendationEngine
from ai_engine.recommendations.recommendation_config import RecommendationConfig
from ai_engine.scoring import ATSScoringEngine


def metric(name: str, score: float, **kwargs: object) -> ComparisonMetric:
    return ComparisonMetric(name=name, score=score, confidence=1.0, **kwargs)


def scored(metrics: list[ComparisonMetric]):
    result = ComparisonResult(overall_score=0, metrics=metrics)
    return result, ATSScoringEngine().score(result)


def test_poor_match_prioritizes_skills_and_keywords() -> None:
    result, ats = scored([
        metric("skills", 10, missing_items=["Docker", "AWS"]), metric("experience", 20),
        metric("keywords", 15, missing_items=["Kubernetes"]), metric("responsibilities", 25),
    ])
    report = RecommendationEngine().generate(result, ats)
    assert report.recommendations[0].id == "missing_skills"
    assert report.recommendations[1].category == "experience"
    assert report.missing_skills == ("Docker", "AWS")
    assert report.keyword_suggestions == ("Kubernetes",)
    assert "poor alignment" in report.summary.lower()


def test_partial_match_uses_medium_priority_without_optional_noise() -> None:
    result, ats = scored([metric(name, 60) for name in ("skills", "experience", "education", "projects", "certifications", "keywords", "responsibilities", "semantic")])
    report = RecommendationEngine().generate(result, ats)
    assert report.recommendations[0].priority == "medium"
    assert {item.category for item in report.recommendations}.isdisjoint({"certifications", "education"})
    assert "moderate alignment" in report.summary.lower()


def test_excellent_match_returns_separate_strengths() -> None:
    result, ats = scored([metric(name, 95) for name in ("skills", "experience", "education", "projects", "certifications", "keywords", "responsibilities", "semantic")])
    report = RecommendationEngine(RecommendationConfig(max_strengths=2)).generate(result, ats)
    assert not any(item.priority in {"critical", "high"} for item in report.recommendations)
    assert len(report.strengths) == 2
    assert all(item.priority == "positive" for item in report.strengths)
    assert "strongly aligned" in report.summary.lower() or "excellent alignment" in report.summary.lower()


def test_missing_skills_are_deduplicated_and_safe() -> None:
    result, ats = scored([metric("skills", 10, missing_items=["AWS", "aws", "Docker"])])
    report = RecommendationEngine(RecommendationConfig(max_missing_skills=1)).generate(result, ats)
    recommendation = next(item for item in report.recommendations if item.id == "missing_skills")
    assert report.missing_skills == ("AWS",)
    assert recommendation.evidence == ("Missing skill: AWS",)
    assert "genuinely used" in recommendation.suggested_actions[0]


def test_keyword_suggestions_are_evidence_based_and_deduplicated() -> None:
    result, ats = scored([metric("keywords", 20, missing_items=["CI/CD", "ci/cd", "Terraform"])])
    report = RecommendationEngine().generate(result, ats)
    recommendation = next(item for item in report.recommendations if item.category == "keywords")
    assert report.keyword_suggestions == ("CI/CD", "Terraform")
    assert "keyword stuffing" in recommendation.suggested_actions[-1]


def test_missing_optional_metrics_and_semantic_are_safe() -> None:
    result, ats = scored([metric("skills", 75)])
    report = RecommendationEngine().generate(result, ats)
    assert not {"projects", "certifications"} & {item.category for item in report.recommendations}
    assert any("Semantic similarity" in warning for warning in report.warnings)


def test_malformed_optional_metric_does_not_stop_valid_output() -> None:
    result = {"metrics": [{"name": "skills", "score": 20, "missing_items": ["Docker"]}, {"name": "keywords", "score": None}]}
    _, ats = scored([metric("skills", 20, missing_items=["Docker"])])
    report = RecommendationEngine().generate(result, ats)
    assert "missing_skills" in {item.id for item in report.recommendations}
    assert any("Keywords comparison data" in warning for warning in report.warnings)


@pytest.mark.parametrize("kwargs", [{"critical_threshold": 60, "high_threshold": 40}, {"max_recommendations": -1}, {"positive_threshold": 101}, {"max_strengths": True}])
def test_invalid_configuration_rejected(kwargs: dict[str, object]) -> None:
    with pytest.raises((TypeError, ValueError)):
        RecommendationConfig(**kwargs)


def test_limits_determinism_and_input_immutability() -> None:
    metrics = [metric("skills", 10, missing_items=["AWS"]), metric("experience", 10), metric("keywords", 10, missing_items=["Docker"]), metric("responsibilities", 10), metric("projects", 10, missing_items=["Project"])]
    result, ats = scored(metrics)
    before_metrics = [item.model_copy(deep=True) for item in result.metrics]
    before_warnings = list(ats.warnings)
    engine = RecommendationEngine(RecommendationConfig(max_recommendations=2))
    first = engine.generate(result, ats)
    assert first == engine.generate(result, ats)
    assert len(first.recommendations) == 2
    assert any("omitted" in warning for warning in first.warnings)
    assert result.metrics == before_metrics
    assert ats.warnings == before_warnings


def test_unknown_metric_is_ignored_and_warnings_are_deduplicated() -> None:
    result, ats = scored([metric("skills", 20, missing_items=["AWS"]), metric("unexpected", 50)])
    ats = replace(ats, warnings=["Input warning", " input warning "])
    report = RecommendationEngine().generate(result, ats)
    assert report.warnings.count("Input warning") == 1
    assert any("unsupported" in warning.lower() for warning in report.warnings)
