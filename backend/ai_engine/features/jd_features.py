"""Construction of deterministic explainable job-description feature vectors."""

from __future__ import annotations

from ai_engine.extraction.jd_models import JobDescription
from ai_engine.features.feature_models import FeatureValue, JobDescriptionFeatures
from ai_engine.features.feature_utils import education_level, parse_experience_years


def build_job_features(job: JobDescription) -> JobDescriptionFeatures:
    def feature(value: object, source: str, confidence: float = 1.0) -> FeatureValue:
        return FeatureValue(value=value, source=source, confidence=confidence)
    required = [item.name for item in job.required_skills]
    preferred = [item.name for item in job.preferred_skills]
    nice = [item.name for item in job.nice_to_have_skills]
    years = parse_experience_years(job.experience_required)
    education = education_level(job.education_required)
    return JobDescriptionFeatures(
        required_skills=feature(required, "Required skills section"), preferred_skills=feature(preferred, "Preferred skills section"),
        nice_to_have_skills=feature(nice, "Nice-to-have skills section"), required_skill_count=feature(len(required), "Required skills section"),
        preferred_skill_count=feature(len(preferred), "Preferred skills section"), minimum_experience=feature(years, "Experience section", 1.0 if years is not None else 0.0),
        education_level=feature(education, "Education section", 1.0 if education != "Unknown" else 0.0),
        responsibility_count=feature(len(job.responsibilities), "Responsibilities section"), keyword_count=feature(len(job.keywords), "Keywords extracted from job description"),
    )
