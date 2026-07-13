"""Job description parser and requirement extractor.

Future responsibilities include:

- Required vs. preferred skill classification
- Experience level and years requirement extraction
- Education and certification requirement parsing
- Responsibility and qualification bullet extraction
- Seniority and role title normalization
"""

from typing import Any


class JDParser:
    """Extract structured requirements from job description text."""

    def extract(self, job_description: str) -> dict[str, Any]:
        """Parse job description into structured requirements.

        Args:
            job_description: Raw or cleaned job description text.

        Returns:
            Structured job requirements and metadata.

        Raises:
            NotImplementedError: Extraction logic is not yet implemented.
        """
        # TODO: Classify must-have vs. nice-to-have skills
        # TODO: Extract min/max years of experience
        # TODO: Normalize job titles against a taxonomy
        raise NotImplementedError("Job description parsing is not yet implemented")
