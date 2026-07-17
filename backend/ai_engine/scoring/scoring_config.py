"""Configuration and validation for deterministic ATS scoring weights."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


DEFAULT_SCORING_WEIGHTS: dict[str, float] = {
    "skills": 0.30,
    "experience": 0.25,
    "education": 0.10,
    "projects": 0.10,
    "certifications": 0.05,
    "keywords": 0.10,
    "responsibilities": 0.05,
    "semantic": 0.05,
}


@dataclass(frozen=True)
class ScoringWeights:
    """Configurable category weights used by :class:`ATSScoringEngine`.

    Values may be supplied as proportions (``0.30``) or percentages (``30``).
    Invalid or missing values are ignored by the engine, which falls back to the
    corresponding default and records a warning.
    """

    values: Mapping[str, float] = field(default_factory=lambda: dict(DEFAULT_SCORING_WEIGHTS))


def validate_weights(values: Mapping[str, object] | None) -> tuple[dict[str, float], list[str]]:
    """Return normalized complete weights and non-fatal validation warnings."""
    configured = values or {}
    normalized: dict[str, float] = {}
    warnings: list[str] = []

    for category, default in DEFAULT_SCORING_WEIGHTS.items():
        raw_value = configured.get(category, default)
        try:
            value = float(raw_value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            warnings.append(f"Invalid weight for '{category}'; using default.")
            value = default

        if value < 0:
            warnings.append(f"Negative weight for '{category}'; using default.")
            value = default
        elif value > 1:
            if value <= 100:
                value /= 100
            else:
                warnings.append(f"Invalid weight for '{category}'; using default.")
                value = default
        normalized[category] = value

    total = sum(normalized.values())
    if total <= 0:
        warnings.append("Weights total zero; using default weights.")
        return dict(DEFAULT_SCORING_WEIGHTS), warnings

    return {category: value / total for category, value in normalized.items()}, warnings
