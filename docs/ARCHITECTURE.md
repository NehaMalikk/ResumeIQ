# Architecture

## Overview

HireMatch AI follows **Clean Architecture** with clear separation between the HTTP API layer, business services, and the AI/ML engine. Dependencies flow inward — the API depends on services, services depend on the AI engine, but the AI engine has no knowledge of HTTP or FastAPI.

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (React)                    │
│              Vite + TypeScript + TailwindCSS             │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP (REST)
┌────────────────────────▼────────────────────────────────┐
│                   Backend (FastAPI)                      │
│  ┌──────────┐  ┌────────────┐  ┌──────────────────────┐ │
│  │   API    │→ │  Services  │→ │     AI Engine        │ │
│  │  Layer   │  │   Layer    │  │  (ML/NLP Pipeline)   │ │
│  └──────────┘  └────────────┘  └──────────────────────┘ │
│       │              │                    │              │
│  ┌────▼────┐   ┌─────▼─────┐    ┌────────▼────────┐    │
│  │ Schemas │   │   Core    │    │  Parsers         │    │
│  │ (Pydantic)│  │ (Config,  │    │  Preprocessing   │    │
│  └─────────┘   │  Logging, │    │  Extraction      │    │
│                │  DB, Err) │    │  Matching        │    │
│                └───────────┘    │  Scoring         │    │
│                                 │  Suggestions     │    │
│                                 │  Inference       │    │
│                                 └──────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### API Layer (`app/api/`)

- HTTP route definitions and request/response handling
- Dependency injection wiring via FastAPI `Depends`
- Input validation through Pydantic schemas
- No business logic — delegates to services

### Service Layer (`app/services/`)

- Business logic orchestration
- Coordinates AI engine components for end-to-end workflows
- Transaction boundaries (future database operations)
- Returns Pydantic response schemas

### Schema Layer (`app/schemas/`)

- Pydantic models for API contracts
- Request validation and response serialization
- Shared between API and service layers

### Core Infrastructure (`app/core/`)

- Application factory (`create_app`)
- Structured logging configuration
- Global exception handlers
- SQLAlchemy database session management
- Lifespan events (startup/shutdown)

### Configuration (`app/config/`)

- Environment-based settings via pydantic-settings
- Single source of truth for all configuration
- Cached singleton via `get_settings()`

### AI Engine (`ai_engine/`)

Self-contained ML/NLP pipeline with no FastAPI dependencies:

| Module           | Responsibility                              |
|------------------|---------------------------------------------|
| `parsers/`       | Raw document → text extraction              |
| `preprocessing/` | Text cleaning and tokenization              |
| `extraction/`    | Structured data from resume and JD            |
| `matching/`      | Semantic similarity between resume and JD     |
| `scoring/`       | ATS compatibility scoring                   |
| `suggestions/`   | Actionable improvement recommendations        |
| `inference/`     | End-to-end prediction orchestration           |
| `training/`      | Model training scripts                        |
| `evaluation/`    | Benchmark and metrics                         |
| `datasets/`      | Training/validation data storage              |
| `checkpoints/`   | Model artifact storage                        |

## Request Flow

### Current: `POST /analyze` (Stub)

```
Client → API Route → AnalysisService.analyze() → AnalyzeResponse
```

### Future: Full Pipeline

```
Client (multipart upload)
  │
  ▼
API Route (/analyze)
  │  validate file + JD text
  ▼
AnalysisService
  │
  ├─► Parser (PDF/DOC/Image) ──► raw text
  ├─► TextCleaner ──► cleaned text
  ├─► ResumeParser + JDParser ──► structured data
  ├─► SkillExtractor ──► skill lists
  ├─► SemanticMatcher ──► match scores
  ├─► ATSScorer ──► ATS scores
  └─► RecommendationEngine ──► suggestions
  │
  ▼
AnalyzeResponse (full results)
```

## Dependency Injection

FastAPI's `Depends` system provides DI throughout the application:

```python
# Dependency provider (singleton via lru_cache)
@lru_cache
def get_analysis_service() -> AnalysisService:
    return AnalysisService()

# Route handler injection
@router.post("/analyze")
async def analyze_resume(
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalyzeResponse:
    return service.analyze()
```

Future dependencies will include database sessions, AI engine predictors, and configuration.

## Error Handling Strategy

| Layer        | Strategy                                           |
|--------------|----------------------------------------------------|
| API          | Pydantic validation errors (automatic 422)         |
| Service      | Raise `AppException` subclasses                    |
| Core         | Global handlers return structured JSON errors      |
| AI Engine    | Raise domain-specific exceptions, caught by service |

All unhandled exceptions return a generic 500 with logging — never expose stack traces to clients.

## Configuration Management

Settings are loaded from environment variables and `.env` files:

```
.env → pydantic-settings → Settings dataclass → get_settings() → injected everywhere
```

Environment-specific behavior (reload, debug, log level) is driven by the `ENVIRONMENT` variable.

## Database Strategy

- SQLAlchemy 2.x with declarative models in `app/models/`
- Alembic for schema migrations
- SQLite for local development, PostgreSQL for production
- Session-per-request pattern via `get_db()` dependency

## Testing Strategy

| Level        | Tool     | Scope                              |
|--------------|----------|------------------------------------|
| Unit         | pytest   | Services, AI engine modules        |
| Integration  | pytest   | API endpoints via TestClient         |
| E2E          | Future   | Frontend + backend together          |

Tests use a dedicated `testing` environment with overridden settings via fixtures.

## Frontend Integration

The frontend communicates with the backend via the service layer in `frontend/src/services/api.ts`:

```
VITE_API_BASE_URL → apiFetch('/analyze') → POST /analyze
```

During development, configure a Vite proxy or set `VITE_API_BASE_URL=http://localhost:8000`.

## Deployment Architecture (Future)

```
                    ┌─────────────┐
                    │   Nginx     │
                    │  (reverse   │
                    │   proxy)    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼                         ▼
     ┌────────────────┐        ┌────────────────┐
     │  Frontend      │        │  Backend       │
     │  (static CDN)  │        │  (Uvicorn x N) │
     └────────────────┘        └───────┬────────┘
                                       │
                              ┌────────┼────────┐
                              ▼                 ▼
                     ┌──────────────┐  ┌──────────────┐
                     │  PostgreSQL  │  │  Redis       │
                     │  (data)      │  │  (cache)     │
                     └──────────────┘  └──────────────┘
```

## Key Design Decisions

1. **Monorepo over polyrepo** — frontend and backend evolve together with shared docs
2. **Placeholder-first AI engine** — ship the API contract early, implement ML incrementally
3. **Pydantic everywhere** — type-safe boundaries between all layers
4. **No AI logic in API routes** — keeps HTTP layer thin and testable
5. **AI engine isolation** — can be tested, trained, and deployed independently
