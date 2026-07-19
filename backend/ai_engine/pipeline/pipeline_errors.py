"""Public exceptions raised by the analysis orchestration layer."""


class PipelineError(Exception):
    """Base class for pipeline failures."""


class InputValidationError(PipelineError, ValueError):
    """Raised when analysis inputs are missing, malformed, or unsupported."""


class PipelineStageError(PipelineError):
    """Raised when one named pipeline stage fails unexpectedly."""

    def __init__(self, stage: str, message: str | None = None) -> None:
        self.stage = stage
        super().__init__(message or f"Analysis pipeline failed during the '{stage}' stage.")
