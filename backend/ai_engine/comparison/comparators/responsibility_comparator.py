from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import concept_matches
class ResponsibilityComparator(BaseComparator):
    name = "responsibilities"
    def compare(self, resume_features, jd_features):
        evidence = [str(value) for value in resume_features.responsibility_evidence.value]
        required = [str(value) for value in jd_features.responsibilities.value]
        matched, missing, support = concept_matches(evidence, required)
        score = 100.0 if not required else round(len(matched) / len(required) * 100, 2)
        return ComparisonMetric(name=self.name, score=score, matched_items=matched, missing_items=missing, details="Deterministic responsibility-concept evidence coverage", confidence=1.0 if required else 0.0, metadata={"evidence": support, "applicable": bool(required)})
