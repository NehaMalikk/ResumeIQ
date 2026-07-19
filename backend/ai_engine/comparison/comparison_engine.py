"""Orchestration and configurable aggregation for comparison plugins."""
from __future__ import annotations
import logging
import time
from dataclasses import dataclass, field
from collections.abc import Iterable
from ai_engine.comparison.base_comparator import BaseComparator
from ai_engine.comparison.comparison_models import ComparisonResult
from ai_engine.comparison.comparators import CertificationComparator, EducationComparator, ExperienceComparator, KeywordComparator, ProjectComparator, ResponsibilityComparator, SemanticComparator, SkillComparator
from ai_engine.features.feature_models import JobDescriptionFeatures, ResumeFeatures
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class ComparisonWeights:
    values: dict[str, float] = field(default_factory=lambda: {"skills": .40, "experience": .20, "education": .10, "projects": .08, "certifications": .04, "keywords": .08, "responsibilities": .10})

class ComparisonEngine:
    """Run registered plugins; plugin names and weights are the extension seam."""
    def __init__(self, comparators: Iterable[BaseComparator] | None = None, weights: ComparisonWeights | None = None) -> None:
        self._comparators = list(comparators) if comparators is not None else [SkillComparator(), ExperienceComparator(), EducationComparator(), ProjectComparator(), CertificationComparator(), KeywordComparator(), ResponsibilityComparator(), SemanticComparator()]
        self._weights = (weights or ComparisonWeights()).values
    def compare(self, resume_features: ResumeFeatures, jd_features: JobDescriptionFeatures) -> ComparisonResult:
        logger.info("Comparison started")
        metrics = []
        for comparator in self._comparators:
            started = time.perf_counter()
            try:
                metric = comparator.compare(resume_features, jd_features)
                metric.metadata["execution_ms"] = round((time.perf_counter() - started) * 1000, 3)
                metrics.append(metric)
                logger.info("Comparator executed: %s", comparator.name)
            except Exception:
                logger.exception("Comparator failed: %s", comparator.name)
        applicable = [(metric, self._weights.get(metric.name, 0.0)) for metric in metrics if metric.confidence > 0 and self._weights.get(metric.name, 0.0) > 0]
        total_weight = sum(weight for _, weight in applicable)
        score = round(sum(metric.score * weight for metric, weight in applicable) / total_weight, 2) if total_weight else 0.0
        logger.info("Comparison completed")
        return ComparisonResult(overall_score=score, metrics=metrics, weights=dict(self._weights))
