"""Human-readable, deterministic ATS score explanations."""
from __future__ import annotations

from dataclasses import dataclass


DISPLAY_NAMES: dict[str, str] = {
    "skills": "Skills",
    "experience": "Experience",
    "education": "Education",
    "projects": "Projects",
    "certifications": "Certifications",
    "keywords": "Keywords",
    "responsibilities": "Responsibilities",
    "semantic": "Semantic",
}


@dataclass(frozen=True)
class ScoreBreakdown:
    """Weighted score contributions and a frontend-ready explanation."""

    contributions: dict[str, float]
    maximums: dict[str, float]
    explanation: str

    @classmethod
    def build(cls, contributions: dict[str, float], weights: dict[str, float]) -> "ScoreBreakdown":
        lines = [f"Overall ATS Score: {round(sum(contributions.values()))}", ""]
        for category, display_name in DISPLAY_NAMES.items():
            lines.extend((f"{display_name}:", f"+{contributions[category]:.2f} / {weights[category] * 100:.2f}", ""))
        return cls(
            contributions=dict(contributions),
            maximums={category: weight * 100 for category, weight in weights.items()},
            explanation="\n".join(lines).rstrip(),
        )

    def __str__(self) -> str:
        return self.explanation
