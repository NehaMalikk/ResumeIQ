from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
class CertificationComparator(BaseComparator):
    name = "certifications"
    def compare(self, resume_features, jd_features):
        count = int(resume_features.certification_count.value)
        return ComparisonMetric(name=self.name, score=100.0, details="JD feature vector has no certification requirements", confidence=0.0, metadata={"resume_certification_count": count, "applicable": False})
