"""Applicant Tracking System (ATS) compatibility scoring.

Future responsibilities include:

- Keyword density and placement scoring
- Format compatibility checks (tables, columns, headers)
- Section completeness scoring
- File format and parsing reliability scoring
- Industry-specific ATS rule profiles
"""

from typing import Any


class ATSScorer:
    """Score resume ATS compatibility and keyword alignment."""

    def score(
        self,
        resume_data: dict[str, Any],
        job_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Compute ATS compatibility and keyword match scores.

        Args:
            resume_data: Structured resume extraction output.
            job_data: Structured job description extraction output.

        Returns:
            ATS score breakdown with sub-scores and recommendations.

        Raises:
            NotImplementedError: Scoring logic is not yet implemented.
        """
        # TODO: Define weighted scoring rubric (keywords, format, sections)
        # TODO: Flag ATS-unfriendly elements (images, complex tables)
        # TODO: Benchmark against industry ATS parsing patterns
        raise NotImplementedError("ATS scoring is not yet implemented")
