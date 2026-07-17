from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import ratio
class ResponsibilityComparator(BaseComparator):
    name = "responsibilities"
    def compare(self, resume_features, jd_features):
        actual, required = int(resume_features.responsibility_count.value), int(jd_features.responsibility_count.value)
        return ComparisonMetric(name=self.name, score=ratio(actual, required), details="Responsibility evidence count coverage", confidence=0.5, metadata={"resume_evidence": actual, "job_responsibilities": required})
