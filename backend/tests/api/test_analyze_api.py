from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from ai_engine.parsers.exceptions import InvalidFileType
from ai_engine.pipeline import AnalysisPipeline, InputValidationError, PipelineStageError
from app.api.dependencies import get_analysis_service


RESUME = b"Jane Doe\nSkills\nPython, FastAPI\n"
JD = "Required Skills\nPython, FastAPI"


@pytest.fixture(scope="module")
def pipeline_report():
    return AnalysisPipeline().analyze(resume_text=RESUME.decode(), job_description_text=JD)


@pytest.fixture
def service_client(client: TestClient, pipeline_report):
    service = Mock()
    service.analyze.return_value = pipeline_report
    client.app.dependency_overrides[get_analysis_service] = lambda: service
    yield client, service
    client.app.dependency_overrides.clear()


@pytest.mark.parametrize("filename", ["resume.pdf", "resume.docx", "resume.txt"])
def test_supported_upload_reaches_pipeline_and_is_cleaned(service_client, filename):
    client, service = service_client
    captured: dict[str, Path] = {}

    def analyze(path, job_description):
        captured["path"] = Path(path)
        assert captured["path"].exists()
        assert captured["path"].suffix == Path(filename).suffix
        assert job_description == JD
        return service.analyze.return_value

    service.analyze.side_effect = analyze
    response = client.post("/analyze", files={"resume": (filename, RESUME)}, data={"job_description": JD})
    assert response.status_code == 200
    assert not captured["path"].exists()


def test_response_contains_complete_json_contract(service_client):
    client, _ = service_client
    response = client.post("/analyze", files={"resume": ("resume.txt", RESUME)}, data={"job_description": JD})
    assert response.status_code == 200
    data = response.json()
    assert {"metadata", "ats_score", "comparison", "recommendations", "resume_features", "job_features", "warnings"} <= data.keys()
    assert isinstance(data["ats_score"], dict)
    assert isinstance(data["comparison"]["metrics"], list)
    assert isinstance(data["recommendations"]["warnings"], list)


def test_txt_upload_runs_real_pipeline(client: TestClient):
    response = client.post("/analyze", files={"resume": ("resume.txt", RESUME)}, data={"job_description": JD})
    assert response.status_code == 200
    assert response.json()["metadata"]["parser_used"] == "TextParser"


def test_missing_resume_returns_validation_json(client: TestClient):
    response = client.post("/analyze", data={"job_description": JD})
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/json")


def test_missing_job_description_returns_validation_json(client: TestClient):
    response = client.post("/analyze", files={"resume": ("resume.txt", RESUME)})
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/json")


def test_empty_job_description_is_treated_as_missing(service_client):
    client, service = service_client
    response = client.post("/analyze", files={"resume": ("resume.txt", RESUME)}, data={"job_description": ""})
    assert response.status_code == 422
    service.analyze.assert_not_called()


def test_whitespace_job_description_returns_400(service_client):
    client, service = service_client
    response = client.post("/analyze", files={"resume": ("resume.txt", RESUME)}, data={"job_description": "   "})
    assert response.status_code == 400
    service.analyze.assert_not_called()


def test_empty_resume_returns_400_and_skips_pipeline(service_client):
    client, service = service_client
    response = client.post("/analyze", files={"resume": ("resume.txt", b"")}, data={"job_description": JD})
    assert response.status_code == 400
    service.analyze.assert_not_called()


def test_unsupported_file_maps_to_415(service_client):
    client, service = service_client
    parser_error = InvalidFileType("unsupported")
    validation_error = InputValidationError("unsupported")
    validation_error.__cause__ = parser_error
    service.analyze.side_effect = validation_error
    response = client.post("/analyze", files={"resume": ("resume.exe", RESUME)}, data={"job_description": JD})
    assert response.status_code == 415
    assert response.json() == {"detail": "Unsupported resume file type."}


def test_pipeline_validation_error_maps_to_400(service_client):
    client, service = service_client
    service.analyze.side_effect = InputValidationError("Invalid analysis input.")
    response = client.post("/analyze", files={"resume": ("resume.txt", RESUME)}, data={"job_description": JD})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid analysis input."


def test_pipeline_stage_error_maps_to_safe_500(service_client):
    client, service = service_client
    service.analyze.side_effect = PipelineStageError("resume parsing")
    response = client.post("/analyze", files={"resume": ("resume.pdf", RESUME)}, data={"job_description": JD})
    assert response.status_code == 500
    assert response.json() == {"detail": "Analysis failed during resume parsing."}


def test_unexpected_error_maps_to_generic_500(service_client):
    client, service = service_client
    service.analyze.side_effect = RuntimeError("secret internal detail")
    response = client.post("/analyze", files={"resume": ("resume.pdf", RESUME)}, data={"job_description": JD})
    assert response.status_code == 500
    assert response.json() == {"detail": "Analysis failed unexpectedly."}


def test_openapi_documents_multipart_and_responses(client: TestClient):
    operation = client.get("/openapi.json").json()["paths"]["/analyze"]["post"]
    assert "multipart/form-data" in operation["requestBody"]["content"]
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert {"400", "415", "500"} <= operation["responses"].keys()


def test_health_endpoint_remains_available(client: TestClient):
    assert client.get("/").status_code == 200
