"""Backward-compatible route availability checks."""
from fastapi.testclient import TestClient


def test_analyze_requires_multipart_fields(client: TestClient) -> None:
    response = client.post("/analyze")
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/json")
