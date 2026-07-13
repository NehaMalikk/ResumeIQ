"""Health endpoint tests."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """GET / should return running status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["service"] == "HireMatch AI Backend"
