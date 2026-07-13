"""Skill and competency extraction from resumes and job descriptions.

Future responsibilities include:

- Skill taxonomy mapping (ESCO, O*NET, custom ontologies)
- Synonym and alias resolution (e.g., "JS" → "JavaScript")
- Soft skill vs. hard skill classification
- Proficiency level inference
- Emerging technology detection
"""

from typing import Any


class SkillExtractor:
    """Extract and normalize skills from unstructured text."""

    def extract(self, text: str) -> list[dict[str, Any]]:
        """Identify skills mentioned in the given text.

        Args:
            text: Resume or job description text.

        Returns:
            List of extracted skills with metadata (name, category, confidence).

        Raises:
            NotImplementedError: Skill extraction is not yet implemented.
        """
        # TODO: Maintain a skill ontology / knowledge graph
        # TODO: Use embedding similarity for fuzzy skill matching
        # TODO: Infer implicit skills from job titles and project descriptions
        raise NotImplementedError("Skill extraction is not yet implemented")
