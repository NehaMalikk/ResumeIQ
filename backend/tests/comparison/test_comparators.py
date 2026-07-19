"""Independent comparator coverage and plugin-registry behaviour."""

from ai_engine.comparison import ComparisonEngine, ComparisonWeights
from ai_engine.comparison.comparators import (
    CertificationComparator,
    EducationComparator,
    ExperienceComparator,
    KeywordComparator,
    ProjectComparator,
    ResponsibilityComparator,
)
from ai_engine.extraction.jd_models import JobDescription
from ai_engine.extraction.models import Resume, ResumeEducation, ResumeExperience, ResumeProject
from ai_engine.features import FeatureBuilder


def _vectors() -> tuple[object, object]:
    builder = FeatureBuilder()
    return (
        builder.build_resume_features(Resume(experience=[ResumeExperience(start_date="2019", end_date="2024", description=["Built service"])], education=[ResumeEducation(degree="Master of Science")], projects=[ResumeProject(name="One"), ResumeProject(name="Two")], raw_text="Python " * 10)),
        builder.build_job_features(JobDescription(experience_required="3 years", education_required="Bachelor degree", keywords=["Python", "API"], responsibilities=[])),
    )


def test_count_and_level_comparators_are_deterministic() -> None:
    resume, job = _vectors()
    assert ExperienceComparator().compare(resume, job).score == 100  # type: ignore[arg-type]
    assert EducationComparator().compare(resume, job).score == 100  # type: ignore[arg-type]
    assert ProjectComparator().compare(resume, job).score == 0  # no job evidence to establish relevance
    assert KeywordComparator().compare(resume, job).score == 0  # type: ignore[arg-type]
    assert ResponsibilityComparator().compare(resume, job).score == 100  # type: ignore[arg-type]
    certification = CertificationComparator().compare(resume, job)  # type: ignore[arg-type]
    assert certification.confidence == 0 and certification.metadata["applicable"] is False


def test_engine_accepts_custom_plugins_and_weights() -> None:
    resume, job = _vectors()
    result = ComparisonEngine(comparators=[EducationComparator()], weights=ComparisonWeights(values={"education": 1.0})).compare(resume, job)  # type: ignore[arg-type]
    assert result.overall_score == 100
    assert [metric.name for metric in result.metrics] == ["education"]
    assert "execution_ms" in result.metrics[0].metadata
