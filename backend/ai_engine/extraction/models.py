"""Pydantic data models representing a parsed resume."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ResumeModel(BaseModel):
    """Base model that strips surrounding whitespace from textual values."""

    model_config = ConfigDict(str_strip_whitespace=True)


class PersonalInfo(ResumeModel):
    """Contact details identified in the resume header."""

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None


class ResumeExperience(ResumeModel):
    """A work or volunteer experience entry."""

    company: str | None = None
    title: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: list[str] = Field(default_factory=list)


class ResumeEducation(ResumeModel):
    """An education or qualification entry."""

    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: list[str] = Field(default_factory=list)


class ResumeProject(ResumeModel):
    """A personal, academic, or professional project entry."""

    name: str | None = None
    url: str | None = None
    technologies: list[str] = Field(default_factory=list)
    description: list[str] = Field(default_factory=list)


class ResumeCertification(ResumeModel):
    """A certification, license, or achievement entry."""

    name: str
    issuer: str | None = None
    date: str | None = None


class ResumeLanguage(ResumeModel):
    """A spoken or written language and its optional proficiency."""

    name: str
    proficiency: str | None = None


class ResumeSkill(ResumeModel):
    """A normalized technical skill and its vocabulary category."""

    name: str
    category: str


class Resume(ResumeModel):
    """Structured representation of a resume without scoring or matching data."""

    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: str | None = None
    skills: list[ResumeSkill] = Field(default_factory=list)
    experience: list[ResumeExperience] = Field(default_factory=list)
    projects: list[ResumeProject] = Field(default_factory=list)
    education: list[ResumeEducation] = Field(default_factory=list)
    certifications: list[ResumeCertification] = Field(default_factory=list)
    languages: list[ResumeLanguage] = Field(default_factory=list)
    raw_text: str = ""
