"""Public response schemas for resume analysis."""
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AnalyzeResponse(BaseModel):
    """JSON-safe representation of a complete pipeline report."""

    model_config = ConfigDict(json_schema_extra={"example": {
        "metadata": {"parser_used": "PDFParser", "comparison_plugins_used": ["skills"]},
        "ats_score": {"overall_score": 82.5}, "comparison": {"overall_score": 80.0},
        "recommendations": {"summary": "Strong alignment."},
        "resume_features": {}, "job_features": {}, "warnings": [],
        "processing_time_ms": 24.1, "pipeline_version": "1.0",
    }})

    metadata: dict[str, Any] = Field(description="Non-sensitive pipeline execution metadata.")
    ats_score: dict[str, Any] | None
    comparison: dict[str, Any] | None
    recommendations: dict[str, Any] | None
    resume_features: dict[str, Any]
    job_features: dict[str, Any]
    warnings: list[str]
    processing_time_ms: float
    pipeline_version: str


class AnalyzeErrorResponse(BaseModel):
    """Standard JSON error body returned by FastAPI."""

    detail: str
