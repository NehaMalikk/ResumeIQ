"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.config.settings import Settings
from app.core.application import create_app


@pytest.fixture
def test_settings() -> Settings:
    """Provide test-specific settings."""
    return Settings(
        environment="testing",
        debug=True,
        log_level="DEBUG",
    )


@pytest.fixture
def client(test_settings: Settings) -> TestClient:
    """Provide a FastAPI test client."""
    app = create_app(settings=test_settings)
    return TestClient(app)
