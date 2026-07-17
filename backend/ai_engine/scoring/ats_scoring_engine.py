"""Deterministic conversion of comparison metrics into an ATS score."""
from __future__ import annotations

import logging
import math
import time
from collections.abc import Mapping
from typing import Any

from ai_engine.scoring.score_breakdown import ScoreBreakdown
from ai_engine.scoring.scoring_config import DEFAULT_SCORING_WEIGHTS, ScoringWeights, validate_weights
from ai_engine.scoring.scoring_models import ATSScore

logger = logging.getLogger(__name__)

_CATEGORIES = tuple(DEFAULT_SCORING_WEIGHTS)
_ALIASES = {"responsibility": "responsibilities", "certification": "certifications", "project": "projects", "skill": "skills", "keyword": "keywords"}


def _clamp(value: object, maximum: float = 100.0) -> float | None:
    """Coerce a finite number, clamping it without allowing malformed values."""
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return max(0.0, min(maximum, number))


class ATSScoringEngine:
    """Produce a weighted, explainable ATS score from a comparison result.

    The engine deliberately consumes only comparator output; it does not invoke
    semantic services, models, external APIs, or any non-deterministic process.
    """

    def __init__(self, weights: ScoringWeights | Mapping[str, float] | None = None) -> None:
        values: Mapping[str, object] | None
        if isinstance(weights, ScoringWeights):
            values = weights.values
        else:
            values = weights
        self._weights, self._weight_warnings = validate_weights(values)

    def score(self, comparison_result: Any) -> ATSScore:
        """Score a ComparisonResult safely, including incomplete duck-typed input."""
        started = time.perf_counter()
        warnings = list(self._weight_warnings)
        logger.info("ATS scoring started")
        try:
            if isinstance(comparison_result, Mapping):
                metrics = comparison_result.get("metrics", [])
            else:
                metrics = getattr(comparison_result, "metrics", []) if comparison_result is not None else []
            if not isinstance(metrics, (list, tuple)):
                warnings.append("Comparison metrics are malformed; treating them as empty.")
                metrics = []

            values, confidences = self._read_metrics(metrics, warnings)
            contributions = {category: round(values[category] * self._weights[category], 2) for category in _CATEGORIES}
            category_scores = {category: round(values[category], 2) for category in _CATEGORIES}
            overall_score = round(max(0.0, min(100.0, sum(contributions.values()))), 2)
            confidence = self._confidence(confidences, warnings)
            breakdown = ScoreBreakdown.build(contributions, self._weights)
            result = ATSScore(
                overall_score=overall_score,
                skills_score=category_scores["skills"], experience_score=category_scores["experience"],
                education_score=category_scores["education"], projects_score=category_scores["projects"],
                certifications_score=category_scores["certifications"], keywords_score=category_scores["keywords"],
                responsibilities_score=category_scores["responsibilities"], semantic_score=category_scores["semantic"],
                confidence=confidence, score_breakdown=breakdown, warnings=warnings,
            )
        except Exception:  # Defensive boundary: scoring must never take down analysis.
            logger.exception("Unexpected ATS scoring validation issue")
            warnings.append("Unexpected scoring input; returned a safe zero score.")
            contributions = {category: 0.0 for category in _CATEGORIES}
            result = ATSScore(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ScoreBreakdown.build(contributions, self._weights), warnings)

        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
        if result.warnings:
            logger.warning("ATS scoring warnings: %s", result.warnings)
        logger.info("ATS scoring completed in %sms", elapsed_ms)
        return result

    def _read_metrics(self, metrics: list[Any] | tuple[Any, ...], warnings: list[str]) -> tuple[dict[str, float], list[float]]:
        scores = {category: 0.0 for category in _CATEGORIES}
        confidences: list[float] = []
        seen: set[str] = set()
        for metric in metrics:
            name = metric.get("name") if isinstance(metric, Mapping) else getattr(metric, "name", None)
            if not isinstance(name, str):
                warnings.append("Ignoring comparison metric without a valid name.")
                continue
            category = _ALIASES.get(name.strip().lower(), name.strip().lower())
            if category not in scores:
                warnings.append(f"Ignoring unknown comparison metric '{name}'.")
                continue
            if category in seen:
                warnings.append(f"Ignoring duplicate comparison metric '{category}'.")
                continue
            raw_score = metric.get("score") if isinstance(metric, Mapping) else getattr(metric, "score", None)
            raw_confidence = metric.get("confidence") if isinstance(metric, Mapping) else getattr(metric, "confidence", None)
            score = _clamp(raw_score)
            confidence = _clamp(raw_confidence, 1.0)
            if score is None or confidence is None:
                warnings.append(f"Ignoring malformed '{category}' comparison metric.")
                continue
            scores[category] = score
            confidences.append(confidence)
            seen.add(category)

        for category in _CATEGORIES:
            if category not in seen:
                warnings.append(f"Missing comparison output for '{category}'; scored as 0.")
        return scores, confidences

    @staticmethod
    def _confidence(metric_confidences: list[float], warnings: list[str]) -> float:
        """Combine populated-output coverage with comparator confidence values."""
        if not metric_confidences:
            return 0.0
        coverage = len(metric_confidences) / len(_CATEGORIES)
        mean_confidence = sum(metric_confidences) / len(metric_confidences)
        malformed_penalty = 0.9 if any("malformed" in warning.lower() for warning in warnings) else 1.0
        return round(max(0.0, min(1.0, coverage * mean_confidence * malformed_penalty)), 3)
