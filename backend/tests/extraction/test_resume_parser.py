"""Unit tests for deterministic resume structure extraction."""

from ai_engine.extraction.resume_parser import ResumeParser


def test_parses_typical_software_engineer_resume() -> None:
    resume = ResumeParser().parse(
        """John Doe
Software Engineer
john@example.com | +1 (555) 123-4567 | https://linkedin.com/in/johndoe | https://github.com/johndoe

Professional Summary
Backend engineer building reliable APIs.

Technical Skills
Python, FastAPI, Docker | PostgreSQL

Work Experience
ABC Technologies
Backend Developer
Jan 2022 - Present
- Built REST APIs

Education
B.Tech Computer Science
Example University
2018 - 2022
"""
    )

    assert resume.personal_info.name == "John Doe"
    assert resume.personal_info.email == "john@example.com"
    assert resume.personal_info.linkedin == "https://linkedin.com/in/johndoe"
    assert [(skill.name, skill.category) for skill in resume.skills] == [
        ("Python", "Programming Language"), ("FastAPI", "Framework"),
        ("Docker", "DevOps"), ("PostgreSQL", "Database"),
    ]
    assert resume.experience[0].company == "ABC Technologies"
    assert resume.experience[0].title == "Backend Developer"
    assert resume.experience[0].start_date == "Jan 2022"
    assert resume.education[0].degree == "B.Tech Computer Science"
    assert resume.education[0].institution == "Example University"


def test_parses_data_science_resume_projects_and_languages() -> None:
    resume = ResumeParser().parse(
        """Ada Lovelace
ada@example.com

SKILLS
Python; pandas; scikit-learn

Academic Projects
Customer Churn Predictor
Technologies: Python, pandas, scikit-learn
- Predicted customer churn.

Certifications
Machine Learning Specialization - Coursera - 2025

Languages
English - Fluent, Hindi (Native)
"""
    )

    assert [(skill.name, skill.category) for skill in resume.skills] == [
        ("Python", "Programming Language"), ("Pandas", "Data Science"),
        ("Scikit-Learn", "Machine Learning"),
    ]
    assert resume.projects[0].name == "Customer Churn Predictor"
    assert resume.projects[0].technologies == ["Python", "pandas", "scikit-learn"]
    assert resume.certifications[0].name == "Machine Learning Specialization"
    assert resume.languages[0].proficiency == "Fluent"
    assert resume.languages[1].proficiency == "Native"


def test_parses_minimal_resume_without_sections() -> None:
    resume = ResumeParser().parse("Jane Smith\njane@example.com\n+44 20 7946 0958")

    assert resume.personal_info.name == "Jane Smith"
    assert resume.personal_info.email == "jane@example.com"
    assert resume.skills == []
    assert resume.experience == []


def test_handles_missing_sections_and_unknown_headings() -> None:
    resume = ResumeParser().parse(
        """Sam Taylor
sam@example.com

Notable Things
Won a local hackathon

OBJECTIVE
Seeking a platform engineering role.
"""
    )

    assert resume.summary == "Seeking a platform engineering role."
    assert resume.education == []
    assert resume.certifications == []


def test_recognizes_case_and_whitespace_variations_in_headings() -> None:
    resume = ResumeParser().parse("Pat Lee\n\n   tEcHnIcAl    sKiLlS :  \nGo\nRust\n\n EMPLOYMENT \nAcme\nEngineer")

    assert [skill.name for skill in resume.skills] == ["Go", "Rust"]
    assert resume.experience[0].company == "Acme"


def test_empty_and_malformed_input_never_crashes() -> None:
    parser = ResumeParser()

    assert parser.parse("   \n\t").raw_text == ""
    assert parser.parse(None).personal_info.name is None  # type: ignore[arg-type]
