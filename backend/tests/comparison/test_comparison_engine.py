from ai_engine.comparison import ComparisonEngine
from ai_engine.comparison.comparators import SkillComparator, SemanticComparator
from ai_engine.features import FeatureBuilder
from ai_engine.extraction.jd_models import JobDescription, JobSkill
from ai_engine.extraction.models import Resume, ResumeSkill

def test_skill_comparator_perfect_partial_and_no_match() -> None:
    builder = FeatureBuilder(); resume = builder.build_resume_features(Resume(skills=[ResumeSkill(name="Python", category="Programming Language")]))
    perfect = builder.build_job_features(JobDescription(required_skills=[JobSkill(name="Python", category="Programming Language")]))
    partial = builder.build_job_features(JobDescription(required_skills=[JobSkill(name="Python", category="Programming Language"), JobSkill(name="AWS", category="Cloud")]))
    none = builder.build_job_features(JobDescription(required_skills=[JobSkill(name="AWS", category="Cloud")]))
    assert SkillComparator().compare(resume, perfect).score == 100
    assert SkillComparator().compare(resume, partial).score == 50
    assert SkillComparator().compare(resume, none).score == 0

def test_orchestrator_handles_empty_and_malformed_features() -> None:
    builder = FeatureBuilder(); result = ComparisonEngine().compare(builder.build_resume_features(Resume()), builder.build_job_features(JobDescription()))
    assert result.overall_score >= 0 and len(result.metrics) == 7
    semantic = SemanticComparator().compare(builder.build_resume_features(Resume()), builder.build_job_features(JobDescription()))
    assert semantic.confidence == 0 and semantic.metadata["implemented"] is False
