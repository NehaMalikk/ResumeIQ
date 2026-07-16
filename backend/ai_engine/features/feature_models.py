"""Public Pydantic models for explainable feature engineering output."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FeatureModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class FeatureValue(FeatureModel):
    """A deterministic value with provenance for future explanations."""

    value: Any
    source: str
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: dict[str, Any] | None = None


class ResumeFeatures(FeatureModel):
    skills: FeatureValue
    skill_count: FeatureValue
    programming_languages: FeatureValue
    frameworks: FeatureValue
    databases: FeatureValue
    cloud_tools: FeatureValue
    devops_tools: FeatureValue
    experience_years: FeatureValue
    education_level: FeatureValue
    project_count: FeatureValue
    certification_count: FeatureValue
    responsibility_count: FeatureValue
    keyword_count: FeatureValue
    section_completeness: FeatureValue
    technical_strength: FeatureValue
    resume_length_words: FeatureValue
    estimated_pages: FeatureValue


class JobDescriptionFeatures(FeatureModel):
    required_skills: FeatureValue
    preferred_skills: FeatureValue
    nice_to_have_skills: FeatureValue
    required_skill_count: FeatureValue
    preferred_skill_count: FeatureValue
    minimum_experience: FeatureValue
    education_level: FeatureValue
    responsibility_count: FeatureValue
    keyword_count: FeatureValue
