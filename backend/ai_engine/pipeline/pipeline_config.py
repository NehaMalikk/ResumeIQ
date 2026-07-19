"""Configuration for the deterministic analysis pipeline."""
from dataclasses import dataclass

from ai_engine.pipeline.pipeline_errors import InputValidationError


@dataclass(frozen=True)
class PipelineConfig:
    """Immutable switches controlling optional analysis stages."""

    enable_recommendations: bool = True
    enable_scoring: bool = True
    enable_comparison: bool = True
    collect_metadata: bool = True
    pipeline_version: str = "1.0"

    def __post_init__(self) -> None:
        for name in ("enable_recommendations", "enable_scoring", "enable_comparison", "collect_metadata"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be a bool.")
        if not isinstance(self.pipeline_version, str) or not self.pipeline_version.strip():
            raise InputValidationError("pipeline_version must be a non-empty string.")
