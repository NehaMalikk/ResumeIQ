"""Tokenization utilities for resume and job description text.

Future responsibilities include:

- Sentence and word tokenization
- Skill and entity-aware token boundaries
- Subword tokenization for transformer models
- Language detection and locale-specific rules
"""


class Tokenizer:
    """Tokenize cleaned text for downstream NLP and embedding models."""

    def tokenize(self, text: str) -> list[str]:
        """Split text into tokens suitable for NLP pipelines.

        Args:
            text: Cleaned document text.

        Returns:
            List of tokens.

        Raises:
            NotImplementedError: Tokenization logic is not yet implemented.
        """
        # TODO: Choose tokenizer strategy (rule-based vs. model-based)
        # TODO: Preserve multi-word skill phrases (e.g., "machine learning")
        # TODO: Support batch tokenization for performance
        raise NotImplementedError("Tokenization is not yet implemented")
