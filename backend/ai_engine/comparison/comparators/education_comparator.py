from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import education_score
class EducationComparator(BaseComparator):
    name = "education"
    def compare(self, resume_features, jd_features):
        r, j = str(resume_features.education_level.value), str(jd_features.education_level.value)
        return ComparisonMetric(name=self.name, score=education_score(r, j), details="Normalized education-level comparison", confidence=1.0 if j != "Unknown" else 0.5, metadata={"resume_level": r, "required_level": j})
