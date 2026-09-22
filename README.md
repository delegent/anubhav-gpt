# AnubhavGPT

AnubhavGPT is a portfolio-quality conversational AI application for software-engineering explanations, production-issue analysis, and structured technical resolutions.

Screenshot placeholder: `docs/screenshot.png`

## Features

- React, TypeScript, Vite, Tailwind, TanStack Query frontend.
- FastAPI, Pydantic v2, SQLAlchemy async, Alembic backend.
- LangGraph workflow around a LangChain chat model factory.
- Deterministic fake-model mode for local development, tests, and CI.
- Conversation create, list, select, delete, persistence, and SSE streaming.
- Safe error envelope, request IDs, CORS configuration, and documentation.

## Quick Start With Docker

```bash
make dev
```

Open `http://localhost:5173`. The API is at `http://localhost:8000/api/v1`.

## Quick Start Without Docker

```bash
make setup
cd apps/api && FAKE_LLM=true LLM_PROVIDER=fake uvicorn app.main:app --reload
cd apps/web && npm run dev
```

## Gemini Configuration

Set these when you want real Gemini calls:

```env
FAKE_LLM=false
LLM_PROVIDER=google_genai
LLM_MODEL=gemini-2.5-flash
GOOGLE_API_KEY=your_key_here
```

Never commit `.env` files.

## Commands

- `make setup`: install local dependencies.
- `make dev`: run Docker Compose with PostgreSQL, API, and web.
- `make stop`: stop containers.
- `make migrate`: run Alembic migrations.
- `make test`: backend and frontend tests.
- `make lint`: Ruff and ESLint.
- `make format`: format code.
- `make typecheck`: mypy and frontend production build.
- `make e2e`: Playwright.

## Architecture

The request path is: React UI -> typed API client -> FastAPI route -> Pydantic schema -> service -> LangGraph workflow -> LangChain model -> repository -> validated response or SSE stream.

Authentication is intentionally outside the MVP, so do not deploy this as a public multi-user product without auth, external rate limiting, and per-user data ownership.

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Development](docs/development.md)
- [Testing](docs/testing.md)
- [Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

## Roadmap

Authentication, tool calling, LangGraph human approval interrupts, RAG with citations, LangSmith evaluations, and distributed rate limiting.

## License

License placeholder. Choose a license before public distribution.
