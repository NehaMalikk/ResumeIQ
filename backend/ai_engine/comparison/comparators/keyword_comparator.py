from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import overlap, strings
class KeywordComparator(BaseComparator):
    name = "keywords"
    def compare(self, resume_features, jd_features):
        matched, missing, extra = overlap(strings(resume_features.keywords.value), strings(jd_features.keywords.value))
        required = strings(jd_features.keywords.value)
        score = 100.0 if not required else round(len(matched) / len(required) * 100, 2)
        return ComparisonMetric(name=self.name, score=score, matched_items=matched, missing_items=missing, extra_items=extra, details="Canonical job-keyword coverage", confidence=1.0 if required else 0.0, metadata={"applicable": bool(required)})
