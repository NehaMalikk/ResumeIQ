"""Importable FastAPI application for tooling and validation."""
from app.core.application import create_app

app = create_app()

__all__ = ["app"]
