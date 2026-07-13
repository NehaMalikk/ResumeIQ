"""Resume analysis request and response schemas."""

from pydantic import BaseModel, Field


class AnalyzeResponse(BaseModel):
    """Placeholder response schema for the analyze endpoint."""

    status: str = Field(..., description="Operation status indicator.")
    message: str = Field(..., description="Human-readable response message.")
