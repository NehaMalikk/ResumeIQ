# HireMatch AI

AI-powered resume analyzer — full-stack monorepo with a React frontend and FastAPI backend.

## Repository Structure

```
HIREMATCH-AI/
├── frontend/          # React + TypeScript + Vite + TailwindCSS + shadcn/ui
├── backend/           # Python 3.12 + FastAPI + SQLAlchemy
│   ├── app/           # Application layer (API, services, schemas)
│   └── ai_engine/     # ML/NLP pipeline modules (placeholders)
├── docs/              # Project documentation
└── README.md          # This file
```

## Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python main.py
```

Open [http://localhost:8000](http://localhost:8000) — API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Documentation

- [Project Vision](docs/PROJECT_VISION.md)
- [Roadmap](docs/ROADMAP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## Development

Run both services concurrently during development:

| Service  | URL                        | Command              |
|----------|----------------------------|----------------------|
| Frontend | http://localhost:5173      | `npm run dev`        |
| Backend  | http://localhost:8000      | `python main.py`     |

Set `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env` when connecting the frontend to the backend.

## License

Private — All rights reserved.
