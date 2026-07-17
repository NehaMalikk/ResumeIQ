"""Comparator contract used by the open plugin registry."""
from __future__ import annotations
from abc import ABC, abstractmethod
from ai_engine.comparison.comparison_models import ComparisonMetric
from ai_engine.features.feature_models import JobDescriptionFeatures, ResumeFeatures

class BaseComparator(ABC):
    name: str
    @abstractmethod
    def compare(self, resume_features: ResumeFeatures, jd_features: JobDescriptionFeatures) -> ComparisonMetric: ...
