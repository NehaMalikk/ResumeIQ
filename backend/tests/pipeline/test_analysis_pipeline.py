from pathlib import Path
from unittest.mock import Mock

import pytest

from ai_engine.pipeline import AnalysisPipeline, InputValidationError, PipelineConfig, PipelineStageError


RESUME = """Jane Doe
jane@example.com
Skills
Python, FastAPI, Docker
Experience
Acme Corp
Software Engineer
2020 - Present
Built Python APIs.
"""
JD = """Job Title
Backend Engineer
Required Skills
Python, FastAPI, Docker
Responsibilities
Build and maintain APIs.
"""


def test_successful_end_to_end_report_contains_all_outputs():
    report = AnalysisPipeline().analyze(resume_text=RESUME, job_description_text=JD)
    assert report.resume_features and report.job_features
    assert report.comparison_result is not None
    assert report.ats_score is not None
    assert report.recommendation_report is not None


def test_comparison_output_reaches_scoring():
    scorer = Mock()
    scorer.score.return_value = AnalysisPipeline().analyze(resume_text=RESUME, job_description_text=JD).ats_score
    pipeline = AnalysisPipeline(scoring_engine=scorer)
    report = pipeline.analyze(resume_text=RESUME, job_description_text=JD)
    scorer.score.assert_called_once_with(report.comparison_result)


def test_scoring_output_reaches_recommendations():
    recommender = Mock()
    expected = AnalysisPipeline().analyze(resume_text=RESUME, job_description_text=JD).recommendation_report
    recommender.generate.return_value = expected
    pipeline = AnalysisPipeline(recommendation_engine=recommender)
    report = pipeline.analyze(resume_text=RESUME, job_description_text=JD)
    recommender.generate.assert_called_once_with(report.comparison_result, report.ats_score)


@pytest.mark.parametrize("kwargs", [
    {"job_description_text": JD},
    {"resume_text": "", "job_description_text": JD},
    {"resume_text": RESUME, "job_description_text": ""},
    {"resume_text": RESUME, "resume_path": "missing.pdf", "job_description_text": JD},
])
def test_invalid_inputs(kwargs):
    with pytest.raises(InputValidationError):
        AnalysisPipeline().analyze(**kwargs)


def test_resume_parsing_failure_is_wrapped(tmp_path: Path):
    path = tmp_path / "resume.pdf"
    path.write_bytes(b"invalid")
    parser = Mock()
    parser.extract_text.side_effect = RuntimeError("boom")
    factory = Mock()
    factory.get_parser.return_value = parser
    with pytest.raises(PipelineStageError, match="resume parsing") as raised:
        AnalysisPipeline(parser_factory=factory).analyze(resume_path=path, job_description_text=JD)
    assert isinstance(raised.value.__cause__, RuntimeError)


@pytest.mark.parametrize("dependency,method,stage", [
    ("feature_builder", "build_resume_features", "resume feature building"),
    ("comparison_engine", "compare", "comparison"),
    ("recommendation_engine", "generate", "recommendations"),
])
def test_stage_failure_is_wrapped(dependency, method, stage):
    failing = Mock()
    getattr(failing, method).side_effect = RuntimeError("boom")
    with pytest.raises(PipelineStageError) as raised:
        AnalysisPipeline(**{dependency: failing}).analyze(resume_text=RESUME, job_description_text=JD)
    assert raised.value.stage == stage
    assert isinstance(raised.value.__cause__, RuntimeError)


def test_metadata_and_processing_time_are_populated():
    report = AnalysisPipeline().analyze(resume_text=RESUME, job_description_text=JD)
    assert report.processing_time_ms >= 0
    assert report.pipeline_version == "1.0"
    assert report.metadata["parser_used"] == "TextParser"
    assert report.metadata["comparison_plugins_used"]
    with pytest.raises(TypeError):
        report.metadata["new"] = "value"  # type: ignore[index]


def test_deterministic_analysis_excluding_timing_metadata():
    pipeline = AnalysisPipeline()
    first = pipeline.analyze(resume_text=RESUME, job_description_text=JD)
    second = pipeline.analyze(resume_text=RESUME, job_description_text=JD)
    assert first.resume_features == second.resume_features
    assert first.job_features == second.job_features
    assert first.ats_score == second.ats_score
    assert first.recommendation_report == second.recommendation_report
    assert first.warnings == second.warnings


def test_recommendations_can_be_disabled():
    recommender = Mock()
    report = AnalysisPipeline(PipelineConfig(enable_recommendations=False), recommendation_engine=recommender).analyze(resume_text=RESUME, job_description_text=JD)
    assert report.recommendation_report is None
    recommender.generate.assert_not_called()


def test_disabling_scoring_skips_downstream_recommendations():
    recommender = Mock()
    report = AnalysisPipeline(PipelineConfig(enable_scoring=False), recommendation_engine=recommender).analyze(resume_text=RESUME, job_description_text=JD)
    assert report.ats_score is None and report.recommendation_report is None
    assert any("Scoring was disabled" in warning for warning in report.warnings)
    recommender.generate.assert_not_called()


def test_warnings_are_aggregated_without_duplicates():
    report = AnalysisPipeline().analyze(resume_text=RESUME, job_description_text=JD)
    assert set(report.ats_score.warnings).issubset(report.warnings)  # type: ignore[union-attr]
    assert set(report.recommendation_report.warnings).issubset(report.warnings)  # type: ignore[union-attr]
    assert len(report.warnings) == len(set(report.warnings))


def test_metadata_collection_can_be_disabled():
    report = AnalysisPipeline(PipelineConfig(collect_metadata=False)).analyze(resume_text=RESUME, job_description_text=JD)
    assert dict(report.metadata) == {}


def test_pipeline_config_validation():
    with pytest.raises(TypeError):
        PipelineConfig(enable_scoring=1)  # type: ignore[arg-type]
    with pytest.raises(InputValidationError):
        PipelineConfig(pipeline_version=" ")
