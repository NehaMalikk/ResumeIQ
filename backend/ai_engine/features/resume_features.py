"""Construction of deterministic explainable resume feature vectors."""

from __future__ import annotations

from ai_engine.extraction.models import Resume
from ai_engine.features.feature_models import FeatureValue, ResumeFeatures
from ai_engine.features.feature_utils import estimate_pages, highest_education, section_completeness, technical_strength, word_count


def build_resume_features(resume: Resume) -> ResumeFeatures:
    skills = [skill.name for skill in resume.skills]
    categories: dict[str, list[str]] = {}
    for skill in resume.skills: categories.setdefault(skill.category, []).append(skill.name)
    years = _experience_years(resume)
    education = highest_education([item.degree for item in resume.education])
    responsibilities = sum(len(item.description) for item in resume.experience) + sum(len(item.description) for item in resume.projects)
    present = sum(bool(value) for value in (resume.personal_info.name, resume.summary, resume.skills, resume.experience, resume.projects, resume.education, resume.certifications, resume.languages))
    source = "Resume sections"
    def feature(value: object, label: str, confidence: float = 1.0, metadata: dict[str, object] | None = None) -> FeatureValue:
        return FeatureValue(value=value, source=label, confidence=confidence, metadata=metadata)
    return ResumeFeatures(
        skills=feature(skills, "Skills section", 1.0), skill_count=feature(len(skills), "Skills section"),
        programming_languages=feature(categories.get("Programming Language", []), "Skills section"),
        frameworks=feature(categories.get("Framework", []), "Skills section"), databases=feature(categories.get("Database", []), "Skills section"),
        cloud_tools=feature(categories.get("Cloud", []), "Skills section"), devops_tools=feature(categories.get("DevOps", []), "Skills section"),
        experience_years=feature(years, "Experience section", 0.75 if years is not None else 0.0),
        education_level=feature(education, "Education section", 1.0 if education != "Unknown" else 0.0),
        project_count=feature(len(resume.projects), "Projects section"), certification_count=feature(len(resume.certifications), "Certifications section"),
        responsibility_count=feature(responsibilities, "Experience and projects sections"), keyword_count=feature(len(set(skills)), "Normalized skills"),
        section_completeness=feature(section_completeness(present, 8), source, 1.0, {"present_sections": present, "total_sections": 8}),
        technical_strength=feature(technical_strength(len(skills), len(categories), len(resume.projects), years, len(resume.certifications)), source, 1.0, {"skill_diversity": len(skills), "category_diversity": len(categories)}),
        resume_length_words=feature(word_count(resume.raw_text), "Raw resume text"), estimated_pages=feature(estimate_pages(word_count(resume.raw_text)), "Raw resume text"),
    )


def _experience_years(resume: Resume) -> float | None:
    """Conservatively sum explicit year-only ranges; ambiguous dates stay absent."""
    total = 0.0
    found = False
    for item in resume.experience:
        if item.start_date and item.end_date:
            import re
            start, end = re.search(r"\b(19|20)\d{2}\b", item.start_date), re.search(r"\b(19|20)\d{2}\b", item.end_date)
            if start and end:
                total += max(0, int(end.group()) - int(start.group()))
                found = True
    return total if found else None
