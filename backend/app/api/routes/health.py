"""Health check route handlers."""

from fastapi import APIRouter, Depends

from app.config.settings import Settings, get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="running", service=settings.app_name)
