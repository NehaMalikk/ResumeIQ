"""Thin application adapter for the analysis pipeline."""
from os import PathLike

from ai_engine.pipeline import AnalysisPipeline, PipelineAnalysisReport
from app.core.logging import get_logger

logger = get_logger(__name__)


class AnalysisService:
    """Expose the pipeline to the HTTP layer without duplicating orchestration."""

    def __init__(self, pipeline: AnalysisPipeline | None = None) -> None:
        self._pipeline = pipeline or AnalysisPipeline()

    def analyze(self, resume_path: str | PathLike[str], job_description: str) -> PipelineAnalysisReport:
        """Delegate one request directly to :class:`AnalysisPipeline`."""
        logger.info("Analysis pipeline execution started")
        report = self._pipeline.analyze(resume_path=resume_path, job_description_text=job_description)
        logger.info("Analysis pipeline execution finished in %sms", report.processing_time_ms)
        return report
