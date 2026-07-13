"""Analyze endpoint tests."""

from fastapi.testclient import TestClient


def test_analyze_placeholder(client: TestClient) -> None:
    """POST /analyze should return placeholder success response."""
    response = client.post("/analyze")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Resume Analyzer pipeline will be implemented here."
