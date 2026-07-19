from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import overlap, strings
class SkillComparator(BaseComparator):
    name = "skills"
    def compare(self, resume_features, jd_features):
        resume = strings(resume_features.skills.value)
        required = strings(jd_features.required_skills.value)
        matched, missing, extra = overlap(resume, required)
        alternatives = {"Redux", "Context API"}
        present_alternatives = alternatives.intersection(required)
        if present_alternatives:
            satisfied = any(item.casefold() in {skill.casefold() for skill in resume} for item in present_alternatives)
            matched = [item for item in matched if item not in alternatives]
            missing = [item for item in missing if item not in alternatives]
            (matched if satisfied else missing).append("Redux or Context API")
        denominator = len(required) - max(0, len(present_alternatives) - 1)
        score = 100.0 if not denominator else round(len(matched) / denominator * 100, 2)
        return ComparisonMetric(name=self.name, score=score, matched_items=matched, missing_items=missing, extra_items=extra, details="Required skill coverage", confidence=1.0 if denominator else 0.0, metadata={"applicable": bool(denominator)})
