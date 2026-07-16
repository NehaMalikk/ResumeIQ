"""Tests for deterministic, explainable feature engineering."""

from ai_engine.extraction.jd_models import JobDescription, JobResponsibility, JobSkill
from ai_engine.extraction.models import Resume, ResumeCertification, ResumeEducation, ResumeExperience, ResumeProject, ResumeSkill
from ai_engine.features import FeatureBuilder


def test_builds_explainable_resume_features() -> None:
    resume = Resume(skills=[ResumeSkill(name="Python", category="Programming Language"), ResumeSkill(name="FastAPI", category="Framework"), ResumeSkill(name="AWS", category="Cloud")], experience=[ResumeExperience(start_date="2020", end_date="2024", description=["Built APIs"])], education=[ResumeEducation(degree="Master of Science")], projects=[ResumeProject(name="API", description=["Designed service"])], certifications=[ResumeCertification(name="AWS Certified")], raw_text="Python developer " * 300)
    features = FeatureBuilder().build_resume_features(resume)
    assert features.skill_count.value == 3
    assert features.experience_years.value == 4
    assert features.education_level.value == "Master"
    assert features.project_count.value == 1
    assert features.estimated_pages.value == 2
    assert 0.0 <= features.technical_strength.value <= 1.0
    assert features.skills.source == "Skills section"


def test_handles_empty_no_projects_many_certifications_and_education_variations() -> None:
    builder = FeatureBuilder()
    empty = builder.build_resume_features(Resume())
    rich = builder.build_resume_features(Resume(projects=[ResumeProject(name=str(index)) for index in range(8)], certifications=[ResumeCertification(name=str(index)) for index in range(6)], education=[ResumeEducation(degree="PhD in Computer Science")]))
    assert empty.skill_count.value == 0 and empty.experience_years.value is None
    assert empty.technical_strength.value == 0.0
    assert rich.project_count.value == 8 and rich.certification_count.value == 6
    assert rich.education_level.value == "PhD"


def test_builds_job_features_for_large_and_missing_skill_jds() -> None:
    job = JobDescription(required_skills=[JobSkill(name="Python", category="Programming Language")], preferred_skills=[JobSkill(name="AWS", category="Cloud")], nice_to_have_skills=[JobSkill(name="Docker", category="DevOps")], experience_required="3+ years", education_required="Bachelor's degree", responsibilities=[JobResponsibility(text="Build APIs")], keywords=["Python", "REST APIs"])
    features = FeatureBuilder().build_job_features(job)
    assert features.required_skill_count.value == 1
    assert features.minimum_experience.value == 3.0
    assert features.education_level.value == "Bachelor"
    assert features.keyword_count.value == 2
    assert FeatureBuilder().build_job_features(JobDescription()).required_skills.value == []
    assert FeatureBuilder().build_resume_features(None).skill_count.value == 0  # type: ignore[arg-type]
