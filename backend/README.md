# HireMatch AI — Backend

Production-ready FastAPI backend for the HireMatch AI resume analyzer platform.

## Tech Stack

- Python 3.12
- FastAPI + Uvicorn
- Pydantic v2 + pydantic-settings
- SQLAlchemy 2.x + Alembic
- Pytest + httpx
- pdfplumber, python-docx, Pillow, pytesseract (document parsing)

## Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` as needed for your local setup.

### 4. Run the Server

```bash
python main.py
```

Or with Uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000).

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method | Path       | Description              |
|--------|------------|--------------------------|
| GET    | `/`        | Health check             |
| POST   | `/analyze` | Resume analysis (stub)   |

### GET `/`

```json
{
  "status": "running",
  "service": "HireMatch AI Backend"
}
```

### POST `/analyze`

```json
{
  "status": "success",
  "message": "Resume Analyzer pipeline will be implemented here."
}
```

## Running Tests

```bash
pytest -v
```

Run parser tests only:

```bash
pytest tests/parsers -v
```

## Document Processing Engine

The `ai_engine/parsers/` package extracts **plain UTF-8 text** from uploaded resume and job description files. It performs no analysis, scoring, or AI processing.

### Supported Formats

| Use Case | Formats |
|----------|---------|
| Resume uploads | PDF, DOC, DOCX, PNG, JPG, JPEG |
| Job descriptions | Plain text, PDF, DOC, DOCX, PNG, JPG, JPEG |

### Parser Architecture

```
Upload file
    │
    ▼
ParserFactory.get_parser(file)   ← detect extension
    │
    ├── .pdf   → PDFParser
    ├── .doc   → DocumentParser
    ├── .docx  → DocumentParser
    ├── .png   → ImageParser
    ├── .jpg   → ImageParser
    ├── .jpeg  → ImageParser
    └── .txt   → TextParser
    │
    ▼
extract_text(...) → plain UTF-8 string
```

Each parser is a single-responsibility class. Shared errors live in `exceptions.py`:

- `InvalidFileType` — unsupported file extension
- `DocumentParsingError` — unreadable, empty, or corrupted documents
- `OCRFailure` — OCR-specific image extraction failures

Logging uses the application logger (`app.core.logging.get_logger`) and records the file name, parser class, and success or failure details.

### Using Parsers

**Automatic parser selection:**

```python
from pathlib import Path

from ai_engine.parsers import ParserFactory, TextParser

file_path = Path("uploads/resume.pdf")
parser = ParserFactory.get_parser(file_path)
text = parser.extract_text(str(file_path))
```

**Plain text job descriptions:**

```python
from ai_engine.parsers import TextParser

parser = TextParser()
clean_jd = parser.extract_text(raw_job_description_text)
```

For `.txt` files, read the file contents first, then pass the string to `TextParser.extract_text`.

**Direct parser usage:**

```python
from ai_engine.parsers import PDFParser, DocumentParser, ImageParser

pdf_text = PDFParser().extract_text("resume.pdf")
doc_text = DocumentParser().extract_text("resume.docx")
image_text = ImageParser().extract_text("scan.png")
```

### OCR Prerequisites

Image parsing requires the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) engine installed on the host system and available on `PATH`. On Windows, install Tesseract and ensure `tesseract.exe` is discoverable by `pytesseract`.

### Legacy DOC Files

`.docx` files are parsed with `python-docx`. Legacy `.doc` files use a best-effort binary decode; for production reliability, prefer DOCX or PDF uploads.

## Resume Structure Extraction (Milestone 2)

`ai_engine/extraction/ResumeParser` converts the plain UTF-8 text produced by the Document Processing Engine into a Pydantic `Resume` object. It is a deterministic structure parser only: it does not score a resume, compare it with a job description, use embeddings, or call an LLM.

### Architecture

```
plain extracted text
        |
        v
ResumeParser.parse(text)
        |
        +-- section detection (normalized conventional headings)
        +-- regex contact/date/URL extraction
        +-- focused section parsers
        v
Resume (Pydantic model)
```

The parser is split into small methods for personal information, summary, skills, experience, projects, education, certifications, and languages. `patterns.py` holds compiled regular expressions, `constants.py` holds supported heading aliases, and `models.py` defines the public Pydantic data model.

### Supported Sections and Models

Recognized headings include Summary/Professional Summary/Objective, Skills/Technical Skills, Experience/Work Experience/Employment/Volunteer Experience, Projects/Academic Projects, Education/Qualifications, Certifications/Achievements, and Languages. Heading matching is case-insensitive and tolerates extra whitespace and a trailing colon.

`Resume` contains `personal_info`, `summary`, `skills`, `experience`, `projects`, `education`, `certifications`, `languages`, and the original `raw_text`. Nested models are `PersonalInfo`, `ResumeExperience`, `ResumeEducation`, `ResumeProject`, `ResumeCertification`, and `ResumeLanguage`.

```python
from ai_engine.extraction import ResumeParser

resume = ResumeParser().parse(extracted_text)
print(resume.personal_info.email)
print(resume.skills)
```

### Limitations

Resume formatting varies substantially. This module uses transparent heuristics and regular expressions, so multi-column extraction artifacts, unconventional headings, or entries without separators can reduce field precision. Missing or ambiguous data remains empty or is preserved as descriptive content. It never raises for empty, malformed, or non-string input.

## Skill Extraction & Normalization Engine (Milestone 3)

`ai_engine/extraction/SkillExtractor` is a reusable, deterministic engine for finding known technical skills in plain text from any source. It does not use embeddings, LLMs, scoring, or semantic matching.

The built-in vocabulary covers programming languages, frameworks, databases, cloud, DevOps, testing, data science, machine learning, AI, security, mobile development, and engineering tools. `SkillNormalizer` maps known aliases and variants such as `py` to `Python`, `ReactJS` to `React`, `Postgres` to `PostgreSQL`, and `AWS Cloud` to `AWS`. Matching is case-insensitive, prefers the longest match, and returns each canonical skill only once in first-occurrence order.

`categories.py` provides `categorize(skill)`, which maps a canonical skill to its category. `ResumeParser` applies this engine only to its existing Skills section and exposes categorized `ResumeSkill` objects:

```python
from ai_engine.extraction import ResumeParser

resume = ResumeParser().parse("""Skills
Python, py, FastAPI, Docker, AWS Cloud, Postgres
""")
print(resume.skills[0].model_dump())
# {"name": "Python", "category": "Programming Language"}
```

## Job Description Structure Extraction (Milestone 4)

`ai_engine/extraction/JobDescriptionParser` turns plain UTF-8 job-description text into a deterministic Pydantic `JobDescription`. It sits directly after document processing and before the future Feature Engineering module. It does not perform feature engineering, embeddings, matching, ATS scoring, recommendations, or use an LLM.

```
plain extracted job-description text
        |
        v
JobDescriptionParser.parse(text)
        +-- heading and list detection
        +-- salary, experience, location, employment/contact extraction
        +-- shared SkillExtractor normalization and categories
        v
JobDescription (ready for future Feature Engineering)
```

The model preserves title, company, location, employment type, department, experience and education requirements, categorized required/preferred/nice-to-have `JobSkill` lists, individual responsibilities, qualifications, benefits, certifications, salary, URLs/emails, keywords, and `raw_text`. `JobRequirement`, `JobResponsibility`, and `JobBenefit` each preserve one source item rather than collapsing a list into a paragraph.

Supported headings are case-insensitive and allow excess whitespace, a trailing colon, bullets, and numbered lists. They include Job Title, About Us/About the Role, Responsibilities, Requirements, Required Skills, Preferred Skills, Nice to Have, Qualifications, Education, Experience, Benefits, Salary, Location, Employment Type, and Department, along with common aliases.

Skills always come from the existing reusable `SkillExtractor`; the JD parser only assigns the existing vocabulary category through `categorize`. This keeps normalization logic in one place and gives future feature engineering stable, categorized inputs.

```python
from ai_engine.extraction import JobDescriptionParser

job = JobDescriptionParser().parse(extracted_text)
print(job.required_skills)
print(job.responsibilities)
```

## Explainable Feature Engineering (Milestone 5)

`ai_engine/features/FeatureBuilder` converts parsed `Resume` and `JobDescription` models into independent, deterministic feature vectors. Every output is a `FeatureValue` with a `value`, `source`, `confidence`, and optional metadata, preserving exactly where future explanations can trace the value.

```
Resume / JobDescription model
        |
        v
FeatureBuilder
        +-- deterministic counts, category grouping, degree normalization
        +-- explicit experience parsing, word/page estimation
        +-- transparent technical-strength heuristic (0.0 to 1.0)
        v
ResumeFeatures / JobDescriptionFeatures
        |
        v
future Semantic Matching (not implemented here)
```

`ResumeFeatures` includes skills grouped by category, experience, education, section completeness, technical strength, document size, and counts. `JobDescriptionFeatures` includes required/preferred/nice-to-have skills, minimum experience, education, responsibility, and keyword features. The builder does not compare documents, score candidates, use embeddings, or call ML/LLM services; future Semantic Matching can consume these typed vectors directly.

```python
from ai_engine.features import FeatureBuilder

features = FeatureBuilder().build_resume_features(resume)
print(features.technical_strength.model_dump())
```

## Comparison Engine (Milestone 6)

`ai_engine/comparison/ComparisonEngine` compares independent `ResumeFeatures` and `JobDescriptionFeatures` using small, deterministic plugins. It produces a `ComparisonResult` containing each `ComparisonMetric` separately plus a weighted aggregate. A metric records its name, 0–100 score, matched/missing/extra items where available, explanatory details, confidence, and metadata.

```
ResumeFeatures + JobDescriptionFeatures
                 |
                 v
          ComparisonEngine
                 |
     +-----------+------------+
     | registered comparator plugins |
     +-- skills, experience, education
     +-- projects, certifications, keywords
     +-- responsibilities
                 |
                 v
     ComparisonResult (metrics + weighted score)
```

Plugins inherit `BaseComparator` and implement `compare(resume_features, jd_features)`. Pass an iterable of comparator instances to `ComparisonEngine` to add, replace, or remove plugins without changing the engine. `ComparisonWeights` centrally configures aggregation; comparator logic does not own weights. Execution time is retained in each metric's metadata and failures are logged without preventing other plugins from running.

`SemanticComparator` is deliberately only a placeholder extension point with zero confidence. It downloads no models and performs no embedding, cosine-similarity, AI, or ML work. Future semantic matching can be introduced as a new plugin while preserving the same `ComparisonMetric` contract.

```python
from ai_engine.comparison import ComparisonEngine

result = ComparisonEngine().compare(resume_features, job_features)
print(result.overall_score)
print(result.metrics[0].model_dump())
```

## Comparison Engine (Milestone 6)

`ai_engine/comparison/ComparisonEngine` compares independently generated `ResumeFeatures` and `JobDescriptionFeatures` through registered comparator plugins. Each plugin implements the `BaseComparator.compare(...)` contract and returns a traceable `ComparisonMetric` with score, matched/missing/extra items, details, confidence, and metadata.

The default deterministic plugins cover skills, experience, education, projects, certifications, keywords, and responsibility evidence. `ComparisonWeights` holds aggregation weights separately from comparator behavior. Plugins can be supplied to the engine constructor, enabling new comparison strategies without modifying orchestration.

The `SemanticComparator` is a zero-confidence placeholder only. No embedding model, similarity calculation, AI, ATS score, or recommendation is implemented in this milestone.

## ATS Scoring Engine (Milestone 7)

`ai_engine/scoring/ATSScoringEngine` converts a `ComparisonResult` into an immutable, explainable `ATSScore`. It is entirely deterministic: it consumes the existing per-category comparison metrics and performs no AI, embeddings, semantic model calls, or external API requests.

```
ComparisonResult (0--100 comparator metrics)
                  |
                  v
          ATSScoringEngine
                  |
                  +-- validate/normalize configurable weights
                  +-- clamp malformed metric values safely
                  +-- calculate weighted contributions
                  +-- calculate output-coverage confidence
                  v
ATSScore (overall score, category scores, explanation, warnings)
```

The default weights are Skills 30%, Experience 25%, Education 10%, Projects 10%, Certifications 5%, Keywords 10%, Responsibilities 5%, and Semantic 5%. Pass `ScoringWeights(values={...})` to configure them. Values may be proportions or whole-number percentages; invalid, negative, missing, or all-zero weights are safely replaced with defaults and noted in `warnings`.

`confidence` is 0.0--1.0 and combines the proportion of the eight expected comparator outputs with their reported comparator confidences. Missing and malformed comparison output therefore still produces a valid result, with a lower confidence and explicit warnings. Every category and aggregate score is clamped to its valid range.

`score_breakdown.explanation` is frontend-ready text showing each category's earned weighted points and maximum contribution:

```python
from ai_engine.scoring import ATSScoringEngine

ats_score = ATSScoringEngine().score(comparison_result)
print(ats_score.overall_score)
print(ats_score.score_breakdown.explanation)
```

## Explainable Recommendation Engine (Milestone 8)

`ai_engine/recommendations/RecommendationEngine` turns a `ComparisonResult` and finalized `ATSScore` into a frontend-ready `RecommendationReport`. It is deterministic and rule-based: it uses no generative AI, LLMs, embeddings, semantic model inference, or external APIs.

```
ComparisonResult + ATSScore
             |
             v
     RecommendationEngine
             |
             +-- prioritized improvements
             +-- strengths
             +-- missing skills and keywords
             +-- section feedback and warnings
```

The frozen report models expose `recommendations`, separate positive `strengths`, `missing_skills`, `keyword_suggestions`, concise `section_feedback`, and frontend-safe `warnings`. Recommendations use evidence from comparison metrics and use finalized ATS component scores for priority. They cover skills, experience, education, projects, certifications, keywords, and responsibilities; optional education and certification feedback appears only when the metric supplies meaningful requirement evidence.

Priorities are `critical`, `high`, `medium`, and `low` by score band, while scores of 85 or above produce separate `positive` strengths. Within a priority, ranking follows configured category importance, score, and stable ID. Case-insensitive deduplication is applied before configured limits; a warning is retained when important findings are truncated. Missing semantic output is a safe availability warning, never a candidate weakness.

```python
from ai_engine.recommendations import RecommendationEngine

report = RecommendationEngine().generate(comparison_result, ats_score)
print(report.summary)
for recommendation in report.recommendations:
    print(recommendation.title, recommendation.evidence)
```

The engine is intentionally independent from FastAPI and the analysis pipeline. A future, opt-in LLM enhancement could improve wording, but should retain these deterministic evidence and safety boundaries.

## Analysis Pipeline (Milestone 9)

`ai_engine.pipeline.AnalysisPipeline` is the single reusable backend entry point for a complete deterministic analysis. It is a thin orchestration layer: parser, extraction, feature, comparison, scoring, and recommendation business logic remains in the existing modules.

```
resume path or text + job-description text
                    |
                    v
             AnalysisPipeline
                    |
     parser -> extraction -> features
                    |
     comparison -> scoring -> recommendations
                    |
                    v
       PipelineAnalysisReport
```

```python
from ai_engine.pipeline import AnalysisPipeline, PipelineConfig

pipeline = AnalysisPipeline(PipelineConfig(enable_recommendations=True))
report = pipeline.analyze(
    resume_path="resume.pdf",
    job_description_text="Required Skills: Python, FastAPI",
)
```

Callers may provide `resume_text` instead of `resume_path`; exactly one is required. The immutable `PipelineAnalysisReport` retains resume and job features, comparison output, ATS score, recommendation report, deduplicated warnings, parser/plugin metadata, processing time, and pipeline version. Disabled stages are represented by `None` rather than fabricated results. Disabling an upstream stage safely skips dependent stages and records a warning.

`PipelineConfig` controls comparison, scoring, recommendations, metadata collection, and the pipeline version. Invalid inputs raise `InputValidationError`. Unexpected engine failures raise `PipelineStageError`, identify the failed stage, and preserve the original exception as `__cause__` without putting stack traces or document contents in report objects.

## FastAPI Analysis Integration (Milestone 10)

`POST /analyze` is the multipart HTTP entry point for the existing `AnalysisPipeline`. The route contains no parsing, extraction, comparison, scoring, or recommendation logic.

```bash
curl -X POST http://localhost:8000/analyze \
  -F "resume=@resume.pdf" \
  -F "job_description=Required Skills: Python, FastAPI"
```

Both fields are required. `resume` accepts the formats supported by `ParserFactory`; `job_description` must contain non-whitespace text. The uploaded file is streamed to a uniquely named operating-system temporary file because document parsers consume filesystem paths. Cleanup runs in a `finally` block after success or failure, and uploaded resumes are never retained.

The response exposes `metadata`, `ats_score`, `comparison`, `recommendations`, `resume_features`, `job_features`, `warnings`, `processing_time_ms`, and `pipeline_version`. A recursive transport serializer converts frozen dataclasses, Pydantic models, tuples, and read-only mappings into JSON-safe objects without changing pipeline models.

Input validation errors return HTTP 400, unsupported extensions return HTTP 415, and pipeline or unexpected failures return safe HTTP 500 JSON responses without tracebacks or document contents. Missing multipart fields use FastAPI's standard HTTP 422 JSON validation response.

Interactive request and response documentation is available at `/docs`; select `POST /analyze`, choose a resume file, enter the job description, and use **Execute**.

## Project Structure

```
backend/
├── app/                    # Application layer (Clean Architecture)
│   ├── api/                # HTTP routes, dependencies, router
│   │   ├── routes/         # Route handlers (health, analyze)
│   │   ├── dependencies.py # Dependency injection providers
│   │   └── router.py       # Aggregated API router
│   ├── core/               # Infrastructure (app factory, logging, DB, errors)
│   ├── config/             # Settings and environment configuration
│   ├── services/           # Business logic orchestration
│   ├── schemas/            # Pydantic request/response models
│   ├── models/             # SQLAlchemy ORM models (placeholder)
│   └── utils/              # Shared helpers
├── ai_engine/              # ML/NLP pipeline (placeholder modules)
│   ├── parsers/            # PDF, DOC, image document parsers
│   ├── preprocessing/      # Text cleaning and tokenization
│   ├── extraction/         # Resume/JD/skill extraction
│   ├── matching/           # Semantic resume-JD matching
│   ├── scoring/            # ATS compatibility scoring
│   ├── suggestions/        # Improvement recommendations
│   ├── datasets/           # Training datasets (not committed)
│   ├── training/           # Model training scripts
│   ├── inference/          # Production inference pipeline
│   ├── evaluation/         # Model evaluation and benchmarks
│   └── checkpoints/        # Model artifacts (not committed)
├── tests/                  # Pytest test suite
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## Architecture Principles

- **Clean Architecture**: API → Services → AI Engine, with schemas defining boundaries
- **SOLID**: Single-responsibility services, dependency injection via FastAPI `Depends`
- **Configuration**: Centralized settings via pydantic-settings with `.env` support
- **Error Handling**: Global exception handlers with structured JSON error responses
- **Logging**: Structured stdout logging with configurable log levels
- **Type Safety**: Full type hints across all modules

## Database Migrations (Alembic)

Alembic is included for future database migrations:

```bash
# Initialize (when models are defined)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Environment Variables

| Variable       | Default                          | Description                    |
|----------------|----------------------------------|--------------------------------|
| `APP_NAME`     | `HireMatch AI Backend`           | Service display name           |
| `APP_VERSION`  | `0.1.0`                          | Application version            |
| `ENVIRONMENT`  | `development`                    | Runtime environment            |
| `DEBUG`        | `false`                          | Enable debug mode              |
| `HOST`         | `0.0.0.0`                        | Server bind host               |
| `PORT`         | `8000`                           | Server bind port               |
| `LOG_LEVEL`    | `INFO`                           | Logging level                  |
| `CORS_ORIGINS` | `http://localhost:5173,...`      | Allowed CORS origins           |
| `DATABASE_URL` | `sqlite:///./hirematch.db`       | SQLAlchemy database URL        |

## Next Steps

1. Wire `AnalysisService` to the `ai_engine.inference.Predictor` pipeline
2. Add multipart file upload handling to `POST /analyze`
3. Define SQLAlchemy models and run Alembic migrations
4. ~~Implement document parsers in `ai_engine/parsers/`~~ (Milestone 1 complete)
5. Connect frontend `VITE_API_BASE_URL` to `http://localhost:8000`
# Deterministic matching accuracy

The analysis pipeline canonicalizes the same bounded skill vocabulary on both
the resume and job-description sides. Variants such as `React.js`/`ReactJS`,
`RESTful APIs`/`REST APIs`, `HTML5`, `CSS3`, `NextJS`, and `Tailwind` resolve to
one canonical value. Boundary-aware extraction keeps Java separate from
JavaScript and C separate from C++ and C#. Resume evidence is collected from
skills, experience, and project text; a technology is never inferred merely
from an adjacent tool or role.

Job skills retain required, preferred, and nice-to-have classification.
`Redux or Context API` is scored as one alternative requirement, so either
technology satisfies the group. Education comparison normalizes degree level
and checks a controlled computing-field group; a B.Tech in Information
Technology therefore meets a bachelor's-in-CS-or-related requirement, while an
unrelated bachelor's degree does not. Recognized month ranges are converted to
non-overlapping inclusive months, and experience credit is the candidate total
divided by the minimum requested experience, capped at full credit.

Responsibilities and projects use explainable controlled concept groups for
component reuse, performance/scalability, REST APIs, collaboration, and
maintainability. Keyword coverage compares unique canonical job terms rather
than raw counts. Metrics with no job requirement (for example certifications)
are marked not applicable. Semantic comparison is explicitly disabled in this
milestone. Neither category contributes points or weight; the ATS denominator
is normalized across applicable metrics without mutating default weights.

The anonymized frontend-engineer regression verifies exact skills, related
education, partial internship duration, project/responsibility evidence,
legitimate Git and Redux/Context gaps, stable recommendations, and deterministic
output. These rules improve exact deterministic correctness but do not provide
semantic understanding; semantic matching remains future work.
