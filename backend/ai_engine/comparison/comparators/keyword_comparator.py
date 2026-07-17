from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import ratio
class KeywordComparator(BaseComparator):
    name = "keywords"
    def compare(self, resume_features, jd_features):
        actual, required = int(resume_features.keyword_count.value), int(jd_features.keyword_count.value)
        return ComparisonMetric(name=self.name, score=ratio(actual, required), details="Normalized keyword-count coverage", confidence=0.4, metadata={"resume_keywords": actual, "job_keywords": required})
