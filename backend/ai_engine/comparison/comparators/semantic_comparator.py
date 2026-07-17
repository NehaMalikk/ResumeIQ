from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
class SemanticComparator(BaseComparator):
    """Reserved extension point; embeddings and models are intentionally absent."""
    name = "semantic"
    def compare(self, resume_features, jd_features):
        return ComparisonMetric(name=self.name, score=0.0, details="Semantic comparison is not implemented", confidence=0.0, metadata={"implemented": False})
