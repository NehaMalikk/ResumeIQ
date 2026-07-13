"""Resume analysis route handlers."""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_analysis_service
from app.schemas.analyze import AnalyzeResponse
from app.services.analysis_service import AnalysisService

router = APIRouter(tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalyzeResponse:
    """Accept resume and job description for analysis.

    The full multipart upload and AI pipeline will be implemented in a future phase.
    """
    return service.analyze()
