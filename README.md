# HireMatch AI

AI-powered resume analyzer frontend — premium SaaS landing experience built with React, TypeScript, and Tailwind CSS.

## Tech Stack

- React 19 + TypeScript
- Tailwind CSS v4
- shadcn/ui patterns (Button, Card, Badge)
- Framer Motion
- Lucide React
- Recharts (ready for dashboard charts)
- Zustand
- React Router v7

## Getting Started

```bash
cd hirematch-ai
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Project Structure

```
src/
├── components/   # UI + landing sections
├── pages/        # Route pages
├── layouts/      # Page layouts
├── hooks/        # Custom hooks
├── store/        # Zustand stores
├── services/     # API layer (backend-ready)
├── utils/        # Utilities (cn, etc.)
├── data/         # Mock JSON data
├── assets/       # Static assets
└── types/        # TypeScript types
```

## Environment

| Variable | Description |
|----------|-------------|
| `VITE_API_BASE_URL` | Backend API base URL (default: `/api`) |

## Scripts

- `npm run dev` — Start dev server
- `npm run build` — Production build
- `npm run preview` — Preview production build
