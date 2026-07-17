"""Typed, explainable results emitted by comparison plugins."""
from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field

class ComparisonMetric(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=100.0)
    matched_items: list[str] = Field(default_factory=list)
    missing_items: list[str] = Field(default_factory=list)
    extra_items: list[str] = Field(default_factory=list)
    details: str = ""
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)

class ComparisonResult(BaseModel):
    overall_score: float = Field(ge=0.0, le=100.0)
    metrics: list[ComparisonMetric] = Field(default_factory=list)
    weights: dict[str, float] = Field(default_factory=dict)
