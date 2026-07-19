"""Immutable public result models for pipeline orchestration."""
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from ai_engine.comparison import ComparisonResult
from ai_engine.features import JobDescriptionFeatures, ResumeFeatures
from ai_engine.recommendations import RecommendationReport
from ai_engine.scoring import ATSScore


@dataclass(frozen=True)
class PipelineAnalysisReport:
    """Complete output of one analysis, including every enabled stage."""

    resume_features: ResumeFeatures
    job_features: JobDescriptionFeatures
    comparison_result: ComparisonResult | None
    ats_score: ATSScore | None
    recommendation_report: RecommendationReport | None
    metadata: Mapping[str, Any]
    processing_time_ms: float
    pipeline_version: str
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
        object.__setattr__(self, "warnings", tuple(self.warnings))
