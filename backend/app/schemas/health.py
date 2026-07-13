"""Health check response schemas."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response schema for the root health endpoint."""

    status: str = Field(..., description="Current service status.")
    service: str = Field(..., description="Human-readable service name.")
