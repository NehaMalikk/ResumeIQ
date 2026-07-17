"""Plugin-based deterministic comparison of resume and job feature vectors."""
from ai_engine.comparison.comparison_engine import ComparisonEngine, ComparisonWeights
from ai_engine.comparison.comparison_models import ComparisonMetric, ComparisonResult
__all__ = ["ComparisonEngine", "ComparisonMetric", "ComparisonResult", "ComparisonWeights"]
