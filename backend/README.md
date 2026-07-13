# HireMatch AI — Backend

Production-ready FastAPI backend for the HireMatch AI resume analyzer platform.

## Tech Stack

- Python 3.12
- FastAPI + Uvicorn
- Pydantic v2 + pydantic-settings
- SQLAlchemy 2.x + Alembic
- Pytest + httpx

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
4. Implement document parsers in `ai_engine/parsers/`
5. Connect frontend `VITE_API_BASE_URL` to `http://localhost:8000`
