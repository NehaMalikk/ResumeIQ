from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.comparison.comparison_utils import ratio
class ProjectComparator(BaseComparator):
    name = "projects"
    def compare(self, resume_features, jd_features):
        projects, responsibilities = int(resume_features.project_count.value), int(jd_features.responsibility_count.value)
        return ComparisonMetric(name=self.name, score=ratio(projects, responsibilities), details="Project count relative to stated responsibilities", confidence=0.5, metadata={"project_count": projects, "responsibility_count": responsibilities})
