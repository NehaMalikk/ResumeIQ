"""Immutable public models returned by the recommendation engine."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class Recommendation:
    """One deterministic, evidence-backed resume recommendation."""

    id: str
    category: str
    priority: str
    title: str
    message: str
    impact: str
    evidence: tuple[str, ...] = ()
    suggested_actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class RecommendationReport:
    """Frontend-ready recommendation output, separate from scoring concerns."""

    summary: str
    overall_score: float
    confidence: float
    recommendations: tuple[Recommendation, ...]
    strengths: tuple[Recommendation, ...]
    missing_skills: tuple[str, ...]
    keyword_suggestions: tuple[str, ...]
    section_feedback: Mapping[str, tuple[str, ...]]
    warnings: tuple[str, ...]

    @classmethod
    def build(cls, **values: object) -> "RecommendationReport":
        """Build a report with a read-only copy of section feedback."""
        feedback = values.pop("section_feedback", {})
        if not isinstance(feedback, Mapping):
            feedback = {}
        values["section_feedback"] = MappingProxyType({key: tuple(item) for key, item in feedback.items()})
        return cls(**values)  # type: ignore[arg-type]
