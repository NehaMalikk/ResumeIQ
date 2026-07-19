# HireMatch AI frontend

React 19 and TypeScript frontend for analyzing a resume against a pasted job description.

## Analyzer flow

The browser temporarily holds the selected resume `File` and sends `POST /api/analyze` as `multipart/form-data`. The request contains exactly:

- `resume`: the uploaded resume file
- `job_description`: trimmed plain text

The browser supplies the multipart boundary. The returned report is held only in `LandingPage` React state and drives the ATS score, comparison, recommendations, strengths, warnings, and processing details shown on screen. Refreshing the page clears the selected file and result. Nothing is written to local storage, session storage, IndexedDB, a database, or cloud storage; the backend deletes its temporary upload after processing.

Job descriptions are text-only in this milestone. File upload and browser-side PDF/DOCX parsing are intentionally unavailable.

Supported resume formats match the backend parser factory: PDF, DOC, DOCX, TXT, PNG, JPG, and JPEG. The UI applies a 5 MB convenience limit; backend validation remains authoritative.

## Local development

Start the backend:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

In another terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). Vite proxies `/api/*` to `http://127.0.0.1:8000/*`, so `/api/analyze` reaches the backend `/analyze` route without local CORS configuration.

## Environment

Copy `.env.example` when an override is needed. `VITE_API_BASE_URL` defaults to `/api`; deployed environments can set it to their API origin. Trailing slashes are normalized. Do not commit real `.env` files or secrets.

## Errors and cancellation

HTTP 400, 415, 422, and 500 responses are mapped to safe user messages. Safe backend string details are retained for client errors; raw objects, HTML, stack traces, and internal server details are not displayed. Network failures are reported separately. Changing either input or unmounting the analyzer aborts the active request, clears an old result, and prevents stale responses from appearing.

## Scripts

- `npm run dev` — start Vite
- `npm run lint` — run ESLint
- `npm run build` — type-check and create a production build
- `npm run preview` — preview the production build
