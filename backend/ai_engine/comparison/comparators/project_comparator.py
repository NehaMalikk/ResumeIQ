from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import concept_matches, overlap, strings
class ProjectComparator(BaseComparator):
    name = "projects"
    def compare(self, resume_features, jd_features):
        projects = [str(value) for value in resume_features.project_evidence.value]
        required_skills = strings(jd_features.required_skills.value)
        project_text = " ".join(projects)
        from ai_engine.extraction.skill_extractor import SkillExtractor
        matched_skills, _, _ = overlap(SkillExtractor().extract(project_text), required_skills)
        matched_resp, _, evidence = concept_matches(projects, strings(jd_features.responsibilities.value))
        evidence_total = len(required_skills) + len(strings(jd_features.responsibilities.value))
        denominator = max(1, evidence_total)
        score = round(min(1.0, (len(matched_skills) + len(matched_resp)) / denominator) * 100, 2) if projects else 0.0
        return ComparisonMetric(name=self.name, score=score, matched_items=[*matched_skills, *matched_resp], details="Project technology and responsibility evidence relevance", confidence=1.0 if evidence_total else 0.0, metadata={"project_count": len(projects), "evidence": evidence, "applicable": bool(evidence_total)})
