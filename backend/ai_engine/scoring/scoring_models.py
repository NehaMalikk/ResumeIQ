"""Public typed result models for ATS scoring."""
from __future__ import annotations

from dataclasses import dataclass, field

from ai_engine.scoring.score_breakdown import ScoreBreakdown


@dataclass(frozen=True)
class ATSScore:
    """Explainable ATS compatibility result, with all scores bounded to 0--100."""

    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    projects_score: float
    certifications_score: float
    keywords_score: float
    responsibilities_score: float
    semantic_score: float
    confidence: float
    score_breakdown: ScoreBreakdown
    warnings: list[str] = field(default_factory=list)
