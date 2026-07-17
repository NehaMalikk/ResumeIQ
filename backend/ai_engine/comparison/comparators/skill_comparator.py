from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import overlap, strings
class SkillComparator(BaseComparator):
    name = "skills"
    def compare(self, resume_features, jd_features):
        matched, missing, extra = overlap(strings(resume_features.skills.value), strings(jd_features.required_skills.value))
        score = 100.0 if not jd_features.required_skills.value else round(len(matched) / len(jd_features.required_skills.value) * 100, 2)
        return ComparisonMetric(name=self.name, score=score, matched_items=matched, missing_items=missing, extra_items=extra, details="Required skill coverage", confidence=1.0)
