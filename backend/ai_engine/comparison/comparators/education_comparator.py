from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import education_score
class EducationComparator(BaseComparator):
    name = "education"
    def compare(self, resume_features, jd_features):
        r, j = str(resume_features.education_level.value), str(jd_features.education_level.value)
        requirement = str(jd_features.education_requirement.value or "")
        details = [str(value) for value in resume_features.education_details.value]
        level_score = education_score(r, j)
        computing = ("computer science", "computer engineering", "information technology", "software engineering", "computer applications")
        field_required = any(term in requirement.casefold() for term in computing) or "related field" in requirement.casefold()
        field_match = any(any(term in value.casefold() for term in computing) for value in details)
        score = level_score if not field_required or field_match else 0.0
        return ComparisonMetric(name=self.name, score=score, matched_items=details if score else [], missing_items=[] if score else [requirement], details="Normalized degree-level and computing-field comparison", confidence=1.0 if j != "Unknown" else 0.0, metadata={"resume_level": r, "required_level": j, "field_match": field_match, "applicable": j != "Unknown"})
