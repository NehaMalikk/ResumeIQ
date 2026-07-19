"""JSON-safe conversion helpers for immutable pipeline output."""
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from ai_engine.pipeline import PipelineAnalysisReport
from app.schemas.analyze import AnalyzeResponse


def to_json_safe(value: Any) -> Any:
    """Recursively convert dataclasses, Pydantic models, and immutable containers."""
    if isinstance(value, BaseModel):
        return to_json_safe(value.model_dump(mode="json"))
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: to_json_safe(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): to_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [to_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def serialize_analysis_report(report: PipelineAnalysisReport) -> AnalyzeResponse:
    """Map the pipeline report onto the stable HTTP response contract."""
    return AnalyzeResponse(
        metadata=to_json_safe(report.metadata), ats_score=to_json_safe(report.ats_score),
        comparison=to_json_safe(report.comparison_result),
        recommendations=to_json_safe(report.recommendation_report),
        resume_features=to_json_safe(report.resume_features), job_features=to_json_safe(report.job_features),
        warnings=list(report.warnings), processing_time_ms=report.processing_time_ms,
        pipeline_version=report.pipeline_version,
    )
