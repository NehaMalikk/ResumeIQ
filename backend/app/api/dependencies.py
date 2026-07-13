"""FastAPI dependency injection providers."""

from functools import lru_cache

from app.services.analysis_service import AnalysisService


@lru_cache
def get_analysis_service() -> AnalysisService:
    """Provide a singleton AnalysisService instance."""
    return AnalysisService()
