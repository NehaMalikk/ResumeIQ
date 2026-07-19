"""Thin orchestration layer for the complete deterministic analysis workflow."""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any

from ai_engine.comparison import ComparisonEngine, ComparisonResult
from ai_engine.extraction import JobDescriptionParser, ResumeParser
from ai_engine.features import FeatureBuilder
from ai_engine.parsers import ParserFactory, TextParser
from ai_engine.recommendations import RecommendationEngine, RecommendationReport
from ai_engine.scoring import ATSScore, ATSScoringEngine

from .pipeline_config import PipelineConfig
from .pipeline_errors import InputValidationError, PipelineStageError
from .pipeline_models import PipelineAnalysisReport

logger = logging.getLogger(__name__)


class AnalysisPipeline:
    """Coordinate existing analysis engines without adding business logic."""

    def __init__(
        self,
        config: PipelineConfig | None = None,
        *,
        parser_factory: Any = ParserFactory,
        resume_extractor: ResumeParser | None = None,
        job_extractor: JobDescriptionParser | None = None,
        feature_builder: FeatureBuilder | None = None,
        comparison_engine: ComparisonEngine | None = None,
        scoring_engine: ATSScoringEngine | None = None,
        recommendation_engine: RecommendationEngine | None = None,
    ) -> None:
        if config is not None and not isinstance(config, PipelineConfig):
            raise TypeError("config must be a PipelineConfig.")
        self.config = config or PipelineConfig()
        self._parser_factory = parser_factory
        self._resume_extractor = resume_extractor or ResumeParser()
        self._job_extractor = job_extractor or JobDescriptionParser()
        self._feature_builder = feature_builder or FeatureBuilder()
        self._comparison_engine = comparison_engine or ComparisonEngine()
        self._scoring_engine = scoring_engine or ATSScoringEngine()
        self._recommendation_engine = recommendation_engine or RecommendationEngine()

    def analyze(
        self,
        resume_path: str | os.PathLike[str] | None = None,
        job_description_text: str | None = None,
        *,
        resume_text: str | None = None,
        job_description: str | None = None,
    ) -> PipelineAnalysisReport:
        """Run one analysis from either a resume path or already-extracted text."""
        started = time.perf_counter()
        logger.info("Analysis pipeline started")
        jd_text = self._validate_inputs(resume_path, resume_text, job_description_text, job_description)
        warnings: list[str] = []

        if resume_text is not None:
            parsed_text = self._stage("resume parsing", TextParser().extract_text, resume_text)
            parser_name = "TextParser"
        else:
            parser = self._stage("parser selection", self._parser_factory.get_parser, resume_path)
            parser_name = type(parser).__name__
            path = Path(resume_path)  # type: ignore[arg-type]
            parser_input: str = (
                self._stage("resume parsing", path.read_text, encoding="utf-8")
                if isinstance(parser, TextParser)
                else str(path)
            )
            parsed_text = self._stage("resume parsing", parser.extract_text, parser_input)
        if not isinstance(parsed_text, str) or not parsed_text.strip():
            raise PipelineStageError("resume parsing", "Resume parser returned empty or invalid text.")
        logger.info("Resume parsed")

        resume = self._stage("resume extraction", self._resume_extractor.parse, parsed_text)
        logger.info("Resume extracted")
        job = self._stage("job description extraction", self._job_extractor.parse, jd_text)
        logger.info("Job description extracted")
        resume_features = self._stage("resume feature building", self._feature_builder.build_resume_features, resume)
        job_features = self._stage("job feature building", self._feature_builder.build_job_features, job)
        logger.info("Features built")

        comparison: ComparisonResult | None = None
        score: ATSScore | None = None
        recommendations: RecommendationReport | None = None
        if self.config.enable_comparison:
            comparison = self._stage("comparison", self._comparison_engine.compare, resume_features, job_features)
            logger.info("Comparison complete")
        else:
            warnings.append("Comparison was disabled by pipeline configuration.")
        if self.config.enable_scoring and comparison is not None:
            score = self._stage("scoring", self._scoring_engine.score, comparison)
            warnings.extend(score.warnings)
            logger.info("Scoring complete")
        elif self.config.enable_scoring:
            warnings.append("Scoring was skipped because comparison output was unavailable.")
        else:
            warnings.append("Scoring was disabled by pipeline configuration.")
        if self.config.enable_recommendations and comparison is not None and score is not None:
            recommendations = self._stage("recommendations", self._recommendation_engine.generate, comparison, score)
            warnings.extend(recommendations.warnings)
            logger.info("Recommendations complete")
        elif self.config.enable_recommendations:
            warnings.append("Recommendations were skipped because comparison or scoring output was unavailable.")
        else:
            warnings.append("Recommendations were disabled by pipeline configuration.")

        elapsed = round((time.perf_counter() - started) * 1000, 3)
        metadata: dict[str, Any] = {}
        if self.config.collect_metadata:
            metadata = {
                "parser_used": parser_name,
                "comparison_plugins_used": tuple(metric.name for metric in comparison.metrics) if comparison else (),
            }
        report = PipelineAnalysisReport(
            resume_features=resume_features, job_features=job_features,
            comparison_result=comparison, ats_score=score, recommendation_report=recommendations,
            metadata=metadata, processing_time_ms=elapsed,
            pipeline_version=self.config.pipeline_version, warnings=tuple(dict.fromkeys(warnings)),
        )
        logger.info("Analysis pipeline completed in %sms", elapsed)
        return report

    @staticmethod
    def _validate_inputs(resume_path: object, resume_text: object, jd_text: object, jd_alias: object) -> str:
        if resume_path is not None and resume_text is not None:
            raise InputValidationError("Provide either resume_path or resume_text, not both.")
        if resume_path is None and resume_text is None:
            raise InputValidationError("A resume_path or resume_text is required.")
        if resume_text is not None and (not isinstance(resume_text, str) or not resume_text.strip()):
            raise InputValidationError("resume_text must be a non-empty string.")
        if resume_path is not None:
            if not isinstance(resume_path, (str, os.PathLike)):
                raise InputValidationError("resume_path must be a string or path-like object.")
            path = Path(resume_path)
            if not path.is_file():
                raise InputValidationError(f"Resume file does not exist: {path}")
            try:
                ParserFactory.get_parser(path)
            except Exception as exc:
                raise InputValidationError(str(exc)) from exc
        if jd_text is not None and jd_alias is not None:
            raise InputValidationError("Provide job_description_text or job_description, not both.")
        value = jd_text if jd_text is not None else jd_alias
        if not isinstance(value, str) or not value.strip():
            raise InputValidationError("job_description_text must be a non-empty string.")
        return TextParser().extract_text(value)

    @staticmethod
    def _stage(stage: str, operation: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return operation(*args, **kwargs)
        except PipelineStageError:
            raise
        except Exception as exc:
            logger.exception("Analysis pipeline stage failed: %s", stage)
            raise PipelineStageError(stage) from exc
