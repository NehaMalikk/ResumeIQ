from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
class CertificationComparator(BaseComparator):
    name = "certifications"
    def compare(self, resume_features, jd_features):
        count = int(resume_features.certification_count.value)
        required = list(jd_features.certification_requirements.value)
        applicable = bool(required)
        score = 100.0 if applicable and count >= len(required) else 0.0
        return ComparisonMetric(name=self.name, score=score, missing_items=required if applicable and not count else [], details="Certification requirement coverage" if applicable else "No certification requirement", confidence=1.0 if applicable else 0.0, metadata={"resume_certification_count": count, "required": required, "applicable": applicable, "status": "applicable" if applicable else "not_applicable"})
