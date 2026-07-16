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
