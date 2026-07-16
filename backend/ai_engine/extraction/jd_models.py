"""Pydantic models produced by the job-description structure parser."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class JobModel(BaseModel):
    """Base model that normalizes surrounding whitespace in text fields."""

    model_config = ConfigDict(str_strip_whitespace=True)


class JobSkill(JobModel):
    """A normalized skill supplied by the shared skill extraction engine."""

    name: str
    category: str


class JobRequirement(JobModel):
    """One qualification or requirement stated by the employer."""

    text: str


class JobResponsibility(JobModel):
    """One independently stated responsibility."""

    text: str


class JobBenefit(JobModel):
    """One benefit offered with the position."""

    text: str


class JobDescription(JobModel):
    """Structured, deterministic representation of an extracted job description.

    Fields deliberately retain the source terminology and do not contain any
    scoring or matching results, allowing a future feature-engineering layer to
    choose its own transformations.
    """

    title: str | None = None
    company: str | None = None
    location: str | None = None
    employment_type: str | None = None
    department: str | None = None
    experience_required: str | None = None
    education_required: str | None = None
    required_skills: list[JobSkill] = Field(default_factory=list)
    preferred_skills: list[JobSkill] = Field(default_factory=list)
    nice_to_have_skills: list[JobSkill] = Field(default_factory=list)
    responsibilities: list[JobResponsibility] = Field(default_factory=list)
    qualifications: list[JobRequirement] = Field(default_factory=list)
    benefits: list[JobBenefit] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    salary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)
    emails: list[str] = Field(default_factory=list)
    raw_text: str = ""
