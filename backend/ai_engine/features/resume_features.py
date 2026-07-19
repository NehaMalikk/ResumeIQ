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
        education_details=feature([" ".join(filter(None, (item.degree, item.field_of_study))) for item in resume.education], "Education section"),
        project_evidence=feature([" ".join(filter(None, (item.name, *item.technologies, *item.description))) for item in resume.projects], "Projects section"),
        responsibility_evidence=feature([text for item in resume.experience for text in item.description] + [text for item in resume.projects for text in item.description], "Experience and projects sections"),
        keywords=feature(_evidence_keywords(resume), "Normalized resume evidence"),
    )


def _experience_years(resume: Resume) -> float | None:
    """Sum non-overlapping recognized month ranges, inclusive of both months."""
    from datetime import date
    from ai_engine.features.feature_utils import parse_month
    ranges = []
    for item in resume.experience:
        if item.start_date and item.end_date and item.start_date.strip().isdigit() and item.end_date.strip().isdigit():
            ranges.extend((year * 12 + 1, year * 12 + 12) for year in range(int(item.start_date), int(item.end_date)))
            continue
        start, end = parse_month(item.start_date), parse_month(item.end_date, reference=date.today())
        if start and end and end >= start:
            ranges.append((start.year * 12 + start.month, end.year * 12 + end.month))
    months: set[int] = set()
    for start, end in ranges: months.update(range(start, end + 1))
    return round(len(months) / 12, 2) if ranges else None


def _evidence_keywords(resume: Resume) -> list[str]:
    text = resume.raw_text.casefold()
    concepts = {"responsive": ("responsive",), "frontend": ("frontend",), "reusable components": ("reusable", "component"), "performance": ("performance", "page load", "bottleneck"), "scalability": ("scalable", "scalability"), "collaboration": ("collaborat", "cross-functional", "backend engineer"), "maintainability": ("maintainab", "modular")}
    return [*dict.fromkeys([skill.name for skill in resume.skills] + [name for name, aliases in concepts.items() if any(alias in text for alias in aliases)])]
