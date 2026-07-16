"""Facade for explainable deterministic resume and JD feature building."""

from __future__ import annotations

import logging

from ai_engine.extraction.jd_models import JobDescription
from ai_engine.extraction.models import Resume
from ai_engine.features.feature_models import JobDescriptionFeatures, ResumeFeatures
from ai_engine.features.jd_features import build_job_features
from ai_engine.features.resume_features import build_resume_features

logger = logging.getLogger(__name__)


class FeatureBuilder:
    """Build typed feature vectors without comparing a resume to a job."""

    def build_resume_features(self, resume: Resume) -> ResumeFeatures:
        logger.info("Feature generation started for resume")
        try:
            result = build_resume_features(resume if isinstance(resume, Resume) else Resume())
            logger.info("Resume features generated")
            return result
        except Exception:
            logger.exception("Resume feature generation failed")
            return build_resume_features(Resume())

    def build_job_features(self, job: JobDescription) -> JobDescriptionFeatures:
        logger.info("Feature generation started for job description")
        try:
            result = build_job_features(job if isinstance(job, JobDescription) else JobDescription())
            logger.info("JD features generated")
            return result
        except Exception:
            logger.exception("JD feature generation failed")
            return build_job_features(JobDescription())
