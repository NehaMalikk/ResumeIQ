"""Milestone 12 deterministic frontend-engineer accuracy regression."""
from ai_engine.pipeline import AnalysisPipeline

FRONTEND_RESUME_TEXT = """Education:
J.C. Bose University
B.Tech Information Technology

Skills:
C, C++, C#, Python, Java, HTML, CSS, JavaScript, SQL/MySQL, Jupyter, Pandas, NumPy

Experience:
Infowiz
Software Developer Intern
January 2025 to June 2025
Contributed to frontend development using HTML, CSS, JavaScript, and React.js with responsive design.
Built modular and reusable UI components to improve maintainability.
Collaborated with backend engineers, QA testers, and AI developers.
Resolved performance bottlenecks for a scalable user experience.

Projects:
StreamSphere
Technologies: HTML, CSS, JavaScript, React.js
Designed and developed a responsive frontend streaming platform.
Improved page load time through efficient component rendering.
Integrated RESTful APIs for video data and authentication.
"""

FRONTEND_JOB_DESCRIPTION = """Role: Frontend Engineer - React.js
Experience: 1-3 years
Job summary:
Build responsive web applications using React.js.
Responsibilities:
Develop reusable UI components using React.js.
Optimize applications for speed and scalability.
Work with REST APIs.
Write clean and maintainable code.
Collaborate with cross-functional teams.
Requirements:
Bachelor's degree in Computer Science or related field.
1-3 years of React.js experience.
Strong knowledge of JavaScript, HTML, and CSS.
Experience with Git.
Familiarity with Redux or Context API.
Nice to have:
TypeScript
Next.js
Tailwind CSS
"""


def test_frontend_engineer_pipeline_accuracy_is_explainable_and_deterministic() -> None:
    first = AnalysisPipeline().analyze(resume_text=FRONTEND_RESUME_TEXT, job_description_text=FRONTEND_JOB_DESCRIPTION)
    second = AnalysisPipeline().analyze(resume_text=FRONTEND_RESUME_TEXT, job_description_text=FRONTEND_JOB_DESCRIPTION)
    assert first.resume_features.skills.value == second.resume_features.skills.value
    assert {"React", "JavaScript", "HTML", "CSS", "REST API"} <= set(first.resume_features.skills.value)
    assert 0 < first.resume_features.experience_years.value < 1
    metrics = {metric.name: metric for metric in first.comparison_result.metrics}
    for name in ("skills", "education", "experience", "projects", "keywords", "responsibilities"):
        assert metrics[name].score > 0
    assert metrics["experience"].score < 100
    assert metrics["certifications"].metadata["status"] == "not_applicable"
    assert {"React", "JavaScript", "HTML", "CSS", "REST API"} <= set(metrics["skills"].matched_items)
    assert "Git" in metrics["skills"].missing_items
    assert "Redux or Context API" in metrics["skills"].missing_items
    assert 35 < first.ats_score.overall_score < 85
    assert not ({"React", "JavaScript", "HTML", "CSS", "REST API"} & set(first.recommendation_report.missing_skills))
    assert not any("scored as 0" in warning for warning in first.warnings)
    assert first.ats_score.overall_score == second.ats_score.overall_score
