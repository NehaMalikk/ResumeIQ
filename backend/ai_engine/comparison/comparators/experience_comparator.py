from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import ratio
class ExperienceComparator(BaseComparator):
    name = "experience"
    def compare(self, resume_features, jd_features):
        actual, required = resume_features.experience_years.value, jd_features.minimum_experience.value
        score = 100.0 if required is None else ratio(float(actual or 0), float(required))
        return ComparisonMetric(name=self.name, score=score, details="Explicit years-of-experience comparison", confidence=min(resume_features.experience_years.confidence, jd_features.minimum_experience.confidence) if required is not None else 0.0, metadata={"resume_years": actual, "required_years": required, "applicable": required is not None})
