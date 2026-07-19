"""Unit tests for deterministic job-description structure extraction."""

from ai_engine.extraction import JobDescriptionParser


def test_parses_software_engineer_jd_into_feature_ready_structure() -> None:
    job = JobDescriptionParser().parse(
        """Senior Backend Engineer

Required Skills
- Python
- FastAPI
- Docker

Preferred Skills
AWS
Kubernetes

Responsibilities
1. Build REST APIs
2. Design scalable backend systems

Education
Bachelor's Degree in Computer Science

Experience
3+ years

Salary: $120,000 - $150,000 per year
Location: Remote
Employment Type: Full-time
"""
    )

    assert job.title == "Senior Backend Engineer"
    assert [(skill.name, skill.category) for skill in job.required_skills] == [
        ("Python", "Programming Language"), ("FastAPI", "Framework"), ("Docker", "DevOps"), ("REST API", "API")
    ]
    assert [skill.name for skill in job.preferred_skills] == ["AWS", "Kubernetes"]
    assert [item.text for item in job.responsibilities] == ["Build REST APIs", "Design scalable backend systems"]
    assert job.experience_required == "3+ years"
    assert job.education_required == "Bachelor's Degree in Computer Science"
    assert job.salary == "$120,000 - $150,000 per year"
    assert job.location == "Remote"
    assert job.employment_type == "Full-time"
    assert "REST APIs" in job.keywords


def test_parses_frontend_backend_and_ai_specializations() -> None:
    parser = JobDescriptionParser()
    frontend = parser.parse("Frontend Developer\nRequired Skills\nReact\nTypeScript\nCSS")
    backend = parser.parse("Backend Developer\nRequirements\nPython, Django, PostgreSQL\n5 years of experience")
    ai = parser.parse("AI Engineer\nRequired Skills\nPython\nPyTorch\nHugging Face\nNice to Have\nAWS")

    assert [item.name for item in frontend.required_skills] == ["React", "TypeScript", "CSS"]
    assert [item.name for item in backend.required_skills] == ["Python", "Django", "PostgreSQL"]
    assert backend.experience_required == "5 years of experience"
    assert [item.name for item in ai.required_skills] == ["Python", "PyTorch", "Hugging Face"]
    assert [item.name for item in ai.nice_to_have_skills] == ["AWS"]


def test_extracts_metadata_contacts_and_individual_list_items() -> None:
    job = JobDescriptionParser().parse(
        """Job Title: Platform Engineer
Company: Example Corp
Department: Infrastructure
Benefits
• Health insurance
• Flexible leave
Qualifications
- Strong communication
- Bachelor's degree
Certifications
AWS Certified Solutions Architect
Contact us at hiring@example.com or https://example.com/jobs
"""
    )

    assert job.title == "Platform Engineer"
    assert job.company == "Example Corp"
    assert job.department == "Infrastructure"
    assert [item.text for item in job.benefits] == ["Health insurance", "Flexible leave"]
    assert [item.text for item in job.qualifications] == ["Strong communication", "Bachelor's degree"]
    assert job.certifications == ["AWS Certified Solutions Architect", "Contact us at hiring@example.com or https://example.com/jobs"]
    assert job.emails == ["hiring@example.com"]
    assert job.urls == ["https://example.com/jobs"]


def test_handles_minimal_random_missing_and_malformed_input() -> None:
    parser = JobDescriptionParser()

    minimal = parser.parse("Junior Developer")
    random = parser.parse("A stroll through the orchard at sunrise.")
    malformed = parser.parse("REQUIRED SKILLS :\nPython\n\nRESPONSIBILITIES\n- Build services\nunknown heading\ntext")

    assert minimal.title == "Junior Developer"
    assert random.title == "A stroll through the orchard at sunrise."
    assert [skill.name for skill in malformed.required_skills] == ["Python"]
    assert [item.text for item in malformed.responsibilities] == ["Build services", "unknown heading", "text"]
    assert parser.parse(" \n\t").raw_text == ""
    assert parser.parse(None).raw_text == ""  # type: ignore[arg-type]
