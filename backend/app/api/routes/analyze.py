"""Resume analysis HTTP transport."""
import os
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool

from ai_engine.parsers.exceptions import InvalidFileType
from ai_engine.pipeline import InputValidationError, PipelineStageError
from app.api.dependencies import get_analysis_service
from app.core.logging import get_logger
from app.schemas.analyze import AnalyzeErrorResponse, AnalyzeResponse
from app.services.analysis_service import AnalysisService
from app.utils.serialization import serialize_analysis_report

router = APIRouter(tags=["Analysis"])
logger = get_logger(__name__)
_ERROR_RESPONSES = {
    400: {"model": AnalyzeErrorResponse, "description": "Invalid or empty input."},
    415: {"model": AnalyzeErrorResponse, "description": "Unsupported resume format."},
    500: {"model": AnalyzeErrorResponse, "description": "Analysis pipeline failure."},
}


@router.post(
    "/analyze", response_model=AnalyzeResponse, responses=_ERROR_RESPONSES,
    summary="Analyze a resume against a job description",
)
async def analyze_resume(
    resume: Annotated[UploadFile, File(description="Resume file (PDF, DOC, DOCX, PNG, JPG, JPEG, or TXT).")],
    job_description: Annotated[str | None, Form(description="Job description text used for comparison.")],
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalyzeResponse:
    """Persist an upload briefly, invoke the pipeline once, and return JSON."""
    logger.info("Analyze request received")
    if job_description is None or not job_description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job description must not be blank.")
    temporary_path: Path | None = None
    try:
        temporary_path = await _persist_upload(resume)
        report = await run_in_threadpool(service.analyze, temporary_path, job_description)
        return serialize_analysis_report(report)
    except InputValidationError as exc:
        if _caused_by_unsupported_file(exc):
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported resume file type.") from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except PipelineStageError as exc:
        logger.exception("Analysis pipeline failed during stage: %s", exc.stage)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analysis failed during {exc.stage}.") from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected analysis request failure")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Analysis failed unexpectedly.") from exc
    finally:
        await resume.close()
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


async def _persist_upload(upload: UploadFile) -> Path:
    """Copy a non-empty upload to a uniquely named temporary file."""
    suffix = Path(upload.filename or "resume").suffix
    descriptor, name = tempfile.mkstemp(prefix="hirematch-resume-", suffix=suffix)
    path = Path(name)
    size = 0
    try:
        with os.fdopen(descriptor, "wb") as destination:
            while chunk := await upload.read(1024 * 1024):
                size += len(chunk)
                destination.write(chunk)
        if size == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume file must not be empty.")
        return path
    except Exception:
        path.unlink(missing_ok=True)
        raise


def _caused_by_unsupported_file(exc: BaseException) -> bool:
    """Detect an unsupported parser error without exposing its exception chain."""
    current: BaseException | None = exc
    while current is not None:
        if isinstance(current, InvalidFileType):
            return True
        current = current.__cause__
    return False
