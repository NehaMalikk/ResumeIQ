# Roadmap

## Phase 0 — Foundation (Current)

**Status: In Progress**

- [x] Monorepo structure (`frontend/`, `backend/`, `docs/`)
- [x] FastAPI backend with health and analyze stub endpoints
- [x] Clean Architecture scaffolding (API → Services → AI Engine)
- [x] AI engine placeholder modules with documented skeletons
- [x] Configuration management, logging, error handling
- [x] Pytest test suite for existing endpoints
- [ ] Alembic migrations initialized with first schema
- [ ] Frontend connected to backend via `VITE_API_BASE_URL`

## Phase 1 — Document Ingestion

**Target: Q3 2026**

- [ ] PDF text extraction (`ai_engine/parsers/pdf_parser.py`)
- [ ] DOCX parsing (`ai_engine/parsers/doc_parser.py`)
- [ ] Image OCR pipeline (`ai_engine/parsers/image_parser.py`)
- [ ] Text cleaning and normalization (`preprocessing/`)
- [ ] Multipart file upload on `POST /analyze`
- [ ] File validation (type, size, content checks)

## Phase 2 — Information Extraction

**Target: Q4 2026**

- [ ] Resume section detection and structured extraction
- [ ] Job description requirement parsing
- [ ] Skill extraction with taxonomy mapping
- [ ] Pydantic schemas for structured resume/JD data
- [ ] Golden dataset creation for extraction benchmarks

## Phase 3 — Matching & Scoring

**Target: Q1 2027**

- [ ] Embedding model integration for semantic matching
- [ ] ATS keyword scoring engine
- [ ] Section-level match breakdown
- [ ] Gap analysis (missing skills, experience shortfalls)
- [ ] Model evaluation suite with regression tests

## Phase 4 — Recommendations & UX

**Target: Q2 2027**

- [ ] Prioritized improvement suggestion engine
- [ ] Frontend integration with live analysis results
- [ ] Analysis history and persistence (database)
- [ ] Exportable analysis reports (PDF)
- [ ] User authentication (optional accounts)

## Phase 5 — Intelligence & Scale

**Target: Q3 2027**

- [ ] Fine-tuned models on resume-JD domain data
- [ ] Batch analysis API
- [ ] Performance optimization (caching, async pipeline)
- [ ] Monitoring and observability (metrics, tracing)
- [ ] Production deployment (Docker, CI/CD)

## Technical Debt & Infrastructure

| Item                          | Priority | Phase |
|-------------------------------|----------|-------|
| Alembic migration setup       | High     | 0     |
| Docker Compose for local dev  | Medium   | 1     |
| GitHub Actions CI pipeline    | Medium   | 1     |
| API rate limiting             | Low      | 4     |
| Redis caching layer           | Low      | 5     |
