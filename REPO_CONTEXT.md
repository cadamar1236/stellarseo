# StellarSEO — Repository Context

> **Mission**: An AI-powered SEO agency that helps e-commerce brands rank #1 on Google through automated keyword research, content generation, and link building.
> **Version**: Deployed prototype (backend v1.0.0 / frontend SPA)
> **Last Updated**: 2025-02-19

---

## 1. Repository Overview

| Attribute | Value |
|---|---|
| **Root** | `./stellarseo/` |
| **Total source files** | ~20 (Python, JavaScript/JSX, CSS, HTML) |
| **Deployment** | Containerized via Docker Compose (Node-style), but actual codebase is Python FastAPI + React SPA |
| **CI/CD** | Partial — GitHub Actions workflow for tech-debt audit exists but `.github/` directory is absent from workspace |
| **README** | Single-line description only |

---

## 2. Tech Stack

### Backend

| Component | Technology |
|---|---|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI (`>=0.110.0`) |
| **Server** | Uvicorn (`>=0.29.0` with `standard` extras) |
| **ORM** | SQLAlchemy 2.0 (`>=2.0.0`) |
| **Database** | PostgreSQL 15 (`psycopg2-binary >=2.9.0`) |
| **API Style** | RESTful (mock-first — returns hardcoded data when no DATABASE_URL is set) |
| **Entry Point** | `backend/main.py` (465 lines, single-file monolith) |

### Frontend

| Component | Technology |
|---|---|
| **Language** | JavaScript (JSX) |
| **Framework** | React 18 (`^18.3.1`) |
| **Build Tool** | Vite 6 (`^6.0.7`) + `@vitejs/plugin-react` |
| **Icons** | lucide-react (`^0.469.0`) |
| **CSS** | Tailwind CSS (loaded via CDN in `index.html`) |
| **Entry Point** | `frontend/index.html` → `main.jsx` → `App.jsx` |

### Standalone Scripts (not React-bundled)

| File | Purpose |
|---|---|
| `frontend/src/exit-intent.js` | Detects mouse-leaving-viewport, fires A/B-tested popup |
| `frontend/src/ab-testing.js` | A/B test variant assignment (50/50), event tracking via localStorage |
| `frontend/src/abTest.js` | ESM version of A/B testing logic |
| `frontend/src/popup-component.js` | Builds & injects exit-intent modal DOM |
| `frontend/src/stats-dashboard.js` | Bottom-right conversion funnel metrics widget |

---

## 3. Architecture

### Pattern: Hybrid Monolith with Mock-First Data Layer

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React SPA)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │Dashboard  │  │Analytics │  │Keywords  │  │Content   │  ...    │
│  │Content    │  │Placeholder│  │Placeholder│  │Placeholder│       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  apiFetch() — retry wrapper (5 retries, 1.5s delay)        │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP (CORS: all origins allowed)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                            │
│                                                                   │
│  ┌──────────────┐       ┌────────────────────────────────────┐   │
│  │  /api/info    │       │  DATABASE_URL set?                 │   │
│  │  /api/metrics │──────▶│  ┌─── YES ──▶ PostgreSQL (SQLAlchemy) │
│  │  /api/stats   │       │  └─── NO  ──▶ Mock Data (8 recs each)│
│  │  /api/clients │       └────────────────────────────────────┘   │
│  │  /api/campaigns│                                              │
│  │  /api/keywords │                                               │
│  │  /api/content  │                                               │
│  │  /api/backlinks│                                               │
│  │  /api/reports  │                                               │
│  │  /api/chart-data│                                              │
│  └──────────────┘                                                │
└─────────────────────────────────────────────────────────────────┘
```

### Notable Design Decisions

1. **Mock-first development**: All API endpoints return hardcoded data when `DATABASE_URL` is not set. No database required for demo/trial. Mock data includes 8 clients, 8 campaigns, 8 keywords, 8 content pieces, 8 backlinks, 8 reports — all pre-populated with realistic e-commerce data.

2. **Single-file backend**: `backend/main.py` contains everything — models, schemas, routes, mock data, startup logic. This is intentional for a prototype but is a tech-debt concern.

3. **State-based routing (no React Router)**: Page navigation is manual via `currentPage` state in `App.jsx`. Only the dashboard page has real implementation; all other 7 pages render a generic `<PagePlaceholder>`.

4. **No auth layer**: CORS allows all origins (`allow_origins=["*"]`). No authentication or rate limiting.

5. **Pydantic v1 API**: All model `.dict()` calls are Pydantic v1 style (Pydantic v2 uses `.model_dump()`). Code works because version isn't pinned.

---

## 4. Database Schema

All tables are dynamically prefixed with `${COMPANY_SLUG}_` (default: `stellar_seo`). No relationships are explicitly declared — foreign keys exist by convention only.

```
stellar_seo_clients
  id              INTEGER PK
  name            VARCHAR NOT NULL
  domain          VARCHAR NOT NULL
  industry        VARCHAR NOT NULL
  monthly_budget  FLOAT   DEFAULT 0.0
  status          VARCHAR DEFAULT 'active'
  created_at      DATETIME

stellar_seo_campaigns
  id              INTEGER PK
  client_id       INTEGER NOT NULL  (FK by convention → clients.id)
  name            VARCHAR NOT NULL
  target_keyword  VARCHAR NOT NULL
  current_rank    INTEGER DEFAULT 0
  target_rank     INTEGER DEFAULT 1
  progress        FLOAT   DEFAULT 0.0
  status          VARCHAR DEFAULT 'active'
  created_at      DATETIME

stellar_seo_keywords
  id               INTEGER PK
  campaign_id      INTEGER NOT NULL  (FK by convention → campaigns.id)
  keyword          VARCHAR NOT NULL
  search_volume    INTEGER DEFAULT 0
  difficulty       FLOAT   DEFAULT 0.0
  current_position INTEGER DEFAULT 0
  best_position    INTEGER DEFAULT 0

stellar_seo_content
  id           INTEGER PK
  campaign_id  INTEGER NOT NULL  (FK by convention → campaigns.id)
  title        VARCHAR NOT NULL
  content_type VARCHAR NOT NULL
  word_count   INTEGER DEFAULT 0
  status       VARCHAR DEFAULT 'draft'
  created_at   DATETIME

stellar_seo_backlinks
  id               INTEGER PK
  campaign_id      INTEGER NOT NULL  (FK by convention → campaigns.id)
  source_domain    VARCHAR NOT NULL
  target_url       VARCHAR NOT NULL
  domain_authority FLOAT   DEFAULT 0.0
  status           VARCHAR DEFAULT 'pending'
  created_at       DATETIME

stellar_seo_reports
  id           INTEGER PK
  campaign_id  INTEGER NOT NULL  (FK by convention → campaigns.id)
  report_type  VARCHAR NOT NULL
  data         TEXT    DEFAULT '{}'  (JSON string)
  generated_at DATETIME
```

**Migrations**: None. Tables are created on startup via `Base.metadata.create_all()`.

---

## 5. API Endpoints

All served at `http://localhost:8000` (or `__BACKEND_URL__` env):

| Method | Path | Returns |
|---|---|---|
| GET | `/health` | `{"status":"ok","app":"StellarRank","version":"1.0.0"}` |
| GET | `/api/info` | Company name, tagline, team size, founded year |
| GET | `/api/metrics` | Total clients, campaigns, keywords, MRR |
| GET | `/api/stats` | Top-10 keywords, content counts, backlink counts |
| GET | `/api/recent-activity` | Last 8 activity feed entries |
| GET | `/api/chart-data?period=` | Chart data for 7/30/90 day periods |
| GET | `/api/clients` | List all clients (DB or mock) |
| POST | `/api/clients` | Create a new client |
| GET | `/api/campaigns?client_id=` | List campaigns (filtered by client) |
| POST | `/api/campaigns` | Create a new campaign |
| GET | `/api/keywords?campaign_id=` | List keywords (filtered by campaign) |
| POST | `/api/keywords` | Create a new keyword |
| GET | `/api/content?campaign_id=` | List content pieces (filtered by campaign) |
| POST | `/api/content` | Create new content |
| GET | `/api/backlinks?campaign_id=` | List backlinks (filtered by campaign) |
| POST | `/api/backlinks` | Create a new backlink |
| GET | `/api/reports?campaign_id=` | List reports (filtered by campaign) |
| POST | `/api/reports` | Create a new report |

The frontend also calls `/api/dashboard` (aggregate data; may be served by host platform rather than FastAPI).

---

## 6. Key Scripts & Configuration Files

### Backend

| File | Purpose |
|---|---|
| `backend/main.py` | Single-file FastAPI app: models, schemas, routes, mock data (465 lines) |
| `backend/requirements.txt` | Python dependencies (fastapi, uvicorn, sqlalchemy, psycopg2-binary, python-multipart) |

### Frontend

| File | Purpose |
|---|---|
| `frontend/index.html` | HTML shell, loads Tailwind via CDN sets `window.__BACKEND_URL__` |
| `frontend/vite.config.js` | Vite build configuration |
| `frontend/src/main.jsx` | React DOM entry point (wraps App in ErrorBoundary) |
| `frontend/src/App.jsx` | Main SPA: sidebar, topbar, dashboard with KPI cards, SVG charts, activity table (637 lines) |
| `frontend/src/index.css` | Base styles |
| `frontend/src/styles.css` | Additional component styles |
| `frontend/src/exit-intent.js` | Exit-intent detection script (standalone) |
| `frontend/src/ab-testing.js` | A/B test variant assignment (standalone) |
| `frontend/src/abTest.js` | ES module version of A/B testing |
| `frontend/src/popup-component.js` | Exit-intent popup DOM injection |
| `frontend/src/stats-dashboard.js` | Conversion funnel metrics widget |

### Config & Infrastructure

| File | Status | Purpose |
|---|---|---|
| `docker-compose.yml` | ✅ Present | Full stack (app + PostgreSQL 15 + Redis 7) |
| `Dockerfile` | ✅ Present | Node.js 18-alpine container (legacy; actual app is Python) |
| `frontend/vite.config.js` | ✅ Present | Vite build config for React SPA |
| `.env.example` | ❌ Missing | Should document: DATABASE_URL, COMPANY_SLUG, COMPANY_PORT |
| `Makefile` | ❌ Missing | Should define: dev, build, test, deploy targets |
| `tsconfig.json` | ❌ Missing | N/A — frontend uses plain JS (not TypeScript) |

---

## 7. Identified Quick-Win Improvements

### Critical (Agent Team Alignment)

| # | Issue | Impact | Fix |
|---|---|---|---|
| 1 | **Frontend files truncated** — `App.jsx` ends mid-expression at line 637 | Dashboard may not render Quick Actions or final UI elements | Complete the missing JSX in `App.jsx` |
| 2 | **Backend files truncated** — `main.py` ends mid-return at line 465 | `create_report()` route broken | Complete the missing Python in `main.py` |
| 3 | **Package.json** declares TypeScript/Express stack (npm scripts, tsconfig patterns) but actual codebase is Python FastAPI + React JS | Agent confusion; wrong dependency set | Update or remove `package.json` — it misrepresents the project |
| 4 | **Dockerfile** builds a Node.js app but backend is Python | Container won't run | Rewrite Dockerfile for Python FastAPI + Uvicorn |
| 5 | **No `.env.example`** — required env vars undocumented | Onboarding friction | Create `.env.example` with DATABASE_URL, COMPANY_SLUG, COMPANY_PORT |

### High

| # | Issue | Impact | Fix |
|---|---|---|---|
| 6 | **No test framework** — 0 unit/integration tests | No regression safety | Add pytest for backend, Vitest for frontend |
| 7 | **CORS allows all origins** (`allow_origins=["*"]`) | Security risk in production | Restrict to known frontend domains |
| 8 | **No auth/rate limiting** on any endpoint | Abuse vulnerability | Add API key middleware + rate limiting |
| 9 | **Pydantic v1 `.dict()`** calls (should be `.model_dump()` in v2) | Future compatibility | Pin Pydantic v1 or migrate to v2 API |
| 10 | **No Alembic migrations** — tables created via `create_all()` on startup | Schema drift in production | Add Alembic for migration management |

### Medium

| # | Issue | Impact | Fix |
|---|---|---|---|
| 11 | **Only dashboard page has content** — 7 other pages are `<PagePlaceholder>` | Half the app is unusable | Implement analytics, keywords, content, backlinks, rank-tracker, reports, settings pages |
| 12 | **No frontend test setup** in package.json | Can't CI-test UI | Add Vitest + React Testing Library |
| 13 | **Standalone JS scripts** (exit-intent, A/B testing) not wired into React app | Marketing funnel not triggered | Import/initialize in `App.jsx` lifecycle |
| 14 | **No CI/CD pipeline** — no `.github/workflows/` present except tech-debt audit | No automated deployment | Add deploy workflow (build → test → deploy) |
| 15 | **Mock data is disconnected** — no real keyword research, content gen, or link building AI | App is a static demo | Connect OpenAI/Claude APIs for real AI features |

### Low

| # | Issue | Impact | Fix |
|---|---|---|---|
| 16 | **README.md is a one-liner** (160 bytes) | Poor developer onboarding | Expand with setup, architecture, and contribution guide |
| 17 | **`scripts/` folder absent** — deploy.sh, seed-data.js, backup.sh referenced in package.json but don't exist | Broken scripts | Create scripts or remove references |
| 18 | **No health check** in Docker Compose | Container orchestration blind | Add HEALTHCHECK to Dockerfile |
| 19 | **No monitoring/observability** — no Sentry, DataDog, or Prometheus config | No error tracking in production | Integrate Sentry (free tier) |

---

## 8. Running the Project

```bash
# Development (backend)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Development (frontend)
cd frontend
npm install
npm run dev    # Vite dev server on port 5173

# Production (full stack)
docker-compose up --build
```

---

## 9. Agent Team Onboarding Notes

### Operations Agent
- Primary responsibilities: infrastructure audits, workflow design, process optimization
- Key files to monitor: `docker-compose.yml`, `Dockerfile`, `requirements.txt`, `README.md`
- Quick wins: Create `.env.example`, audit Dockerfile for Python mismatch, add Makefile

### Coder Agent
- Primary responsibilities: code changes, file creation, data science tasks
- Key files to maintain: `backend/main.py` (all backend logic), `frontend/src/App.jsx` (all frontend logic)
- Known issues: Both main files are truncated — verify file integrity before editing
- One file per delegation rule applies — split big features into individual file subtasks

---

## 10. Environment Variables

| Variable | Default | Required | Description |
|---|---|---|---|
| `DATABASE_URL` | (none) | No* | PostgreSQL connection string. If absent, mock data is used. |
| `COMPANY_SLUG` | `stellar_seo` | No | Prefix for all database table names |
| `COMPANY_PORT` | `8000` | No | Backend server port |
| `__BACKEND_URL__` | (empty) | No | Frontend JS global — backend API base URL |

*Required for real database mode; optional for demo/mock mode.

---

> **Note to agents**: This file should be kept in sync with the actual codebase. When making architectural changes (adding routes, changing tech stack, modifying DB schema), update this document accordingly.