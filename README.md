# Evertheme — Requirements Backlog App

Convert requirement documents into reviewed, version-controlled backlogs and publish them to your project management tool.

## Features

- Upload requirement documents (.docx, .pdf, .txt, .md)
- AI-powered user story generation (OpenAI, Anthropic, Azure OpenAI, Ollama)
- Automated story review for ambiguity and missing requirements
- Inline story editing with full version history
- One-click export to JIRA, Asana, Trello, or Azure DevOps
- Per-user authentication and project isolation

## Quick Start (Docker)

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY, ENCRYPTION_KEY, and your LLM API keys
docker-compose up --build
```

App will be available at **http://localhost** (port 80, via Nginx).
Port 3000 is not published directly in production mode — Nginx proxies everything.

## Development (hot reload)

```bash
cp .env.example .env
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

- Frontend: http://localhost:3000  ← direct Next.js (dev only)
- Backend API: http://localhost:8000  ← direct FastAPI (dev only)
- API docs: http://localhost:8000/docs

## Environment Variables

See `.env.example` for all required variables.

Key variables:
| Variable | Description |
|---|---|
| `SECRET_KEY` | JWT signing secret (min 32 chars) |
| `ENCRYPTION_KEY` | Fernet key for encrypting PM credentials |
| `DATABASE_URL` | PostgreSQL connection string |
| `OPENAI_API_KEY` | Optional — can also be set per-user in UI |

## Running Tests

Tests run entirely locally — no running Docker or live services required.

### Backend

Uses **pytest** with an in-memory SQLite database (no PostgreSQL needed) and mocked LLM/PM calls.

```bash
cd backend
pip install -r requirements.txt
pytest                          # all tests + coverage report
pytest tests/test_auth.py       # single file
pytest -k "test_login"          # tests matching a name pattern
pytest -x                       # stop on first failure
pytest --no-cov                 # skip coverage (faster)
```

Coverage is reported automatically via `pytest-cov`. The `conftest.py` sets the required `SECRET_KEY` and `ENCRYPTION_KEY` environment variables automatically, so no `.env` file is needed for tests.

### Frontend

Uses **Jest** + **React Testing Library**. API calls are intercepted with `axios-mock-adapter` and Next.js router/navigation is mocked.

```bash
cd frontend
npm install
npm test                        # run all tests once
npm run test:watch              # interactive watch mode
npm run test:coverage           # with coverage report
```

### What is covered

| Area | Backend (pytest) | Frontend (Jest + RTL) |
|---|---|---|
| Authentication | register, login, JWT validation, `/me` | Login page, Register page, `auth.ts` helpers |
| Projects | full CRUD + auth guards | — |
| Documents | upload, multi-format parser, versioning | — |
| Stories | CRUD, versioning, LLM generation, LLM review | StoryCard component |
| LLM providers | factory, all four providers, generator + reviewer | — |
| PM integrations | CRUD, export, credentials not exposed, Asana + Trello | ExportModal component |
| Utilities | Fernet encrypt/decrypt | `cn()`, `formatDate()`, color maps |
| API client | — | Token injection, error propagation |
| Review UI | — | ReviewPanel component |

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **LLM**: OpenAI / Anthropic / Azure OpenAI / Ollama (configurable)
- **PM Integrations**: JIRA, Asana, Trello, Azure DevOps
- **Infrastructure**: Docker Compose, Nginx
