"""Validated configuration for deterministic recommendation rules."""
from __future__ import annotations

from dataclasses import dataclass, field


SUPPORTED_CATEGORIES = ("skills", "experience", "education", "projects", "certifications", "keywords", "responsibilities", "semantic", "resume_quality", "general")
SUPPORTED_PRIORITIES = ("critical", "high", "medium", "low", "positive")
DEFAULT_CATEGORY_ORDER = ("skills", "experience", "keywords", "responsibilities", "projects", "education", "certifications", "semantic", "resume_quality", "general")
DEFAULT_PRIORITY_ORDER = ("critical", "high", "medium", "low", "positive")


@dataclass(frozen=True)
class RecommendationConfig:
    """Score bands, limits, and deterministic ranking preferences."""

    critical_threshold: float = 30.0
    high_threshold: float = 50.0
    medium_threshold: float = 70.0
    positive_threshold: float = 85.0
    max_recommendations: int = 8
    max_strengths: int = 4
    max_missing_skills: int = 10
    max_keyword_suggestions: int = 10
    category_order: tuple[str, ...] = field(default_factory=lambda: DEFAULT_CATEGORY_ORDER)
    priority_order: tuple[str, ...] = field(default_factory=lambda: DEFAULT_PRIORITY_ORDER)

    def __post_init__(self) -> None:
        thresholds = (self.critical_threshold, self.high_threshold, self.medium_threshold, self.positive_threshold)
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in thresholds):
            raise TypeError("Recommendation thresholds must be numeric values.")
        if any(not 0 <= float(value) <= 100 for value in thresholds):
            raise ValueError("Recommendation thresholds must be between 0 and 100.")
        if not thresholds[0] < thresholds[1] < thresholds[2] < thresholds[3]:
            raise ValueError("Recommendation thresholds must be strictly ordered.")
        for name in ("max_recommendations", "max_strengths", "max_missing_skills", "max_keyword_suggestions"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be a non-negative integer.")
            if value < 0:
                raise ValueError(f"{name} must be a non-negative integer.")
        if any(category not in SUPPORTED_CATEGORIES for category in self.category_order):
            raise ValueError("category_order contains an unsupported category.")
        if any(priority not in SUPPORTED_PRIORITIES for priority in self.priority_order):
            raise ValueError("priority_order contains an unsupported priority.")


DEFAULT_RECOMMENDATION_CONFIG = RecommendationConfig()
