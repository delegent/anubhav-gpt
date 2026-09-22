# AnubhavGPT — Production-Standard Codex Build Specification

> Copy this entire document into Codex as the implementation request. Codex must build and verify the application, not merely return a plan.

## 1. Role and execution mandate

You are a senior full-stack and AI platform engineer. Build **AnubhavGPT**, a polished conversational AI web application intended both as a useful product and as a portfolio-quality demonstration of React, FastAPI, Pydantic, LangChain, and LangGraph.

Work autonomously within the repository. Before editing, inspect the repository, existing instructions, package files, and current changes. Preserve unrelated work. If the repository is empty, initialize the project using the structure below.

Do not stop after scaffolding or describing the approach. Implement the application, run it, test it, fix failures, and write complete documentation. If a third-party API key is unavailable, finish everything else and provide a deterministic fake-model mode so the project can still be tested locally and in CI.

Use currently supported, non-deprecated APIs. Consult official documentation when an API may have changed. Do not use legacy LangChain APIs such as `LLMChain`, deprecated memory classes, or obsolete agent executors.

## 2. Product definition

Build a responsive AI assistant named **AnubhavGPT** with the following positioning:

> A software-engineering assistant that explains technical concepts, analyzes production issues, and produces clear, structured resolutions.

The product must feel intentional rather than like a generic ChatGPT clone. Use a refined dark interface, concise typography, excellent spacing, accessible contrast, subtle animation, and clear loading/error states.

### Primary user journeys

1. A user opens the application and sees a welcome state with starter prompts.
2. The user creates a conversation and sends a message.
3. The backend validates the request with Pydantic.
4. A LangGraph workflow invokes a LangChain chat model.
5. The answer streams to the browser.
6. The conversation remains available after refresh.
7. The user can create, rename, select, and delete conversations.
8. Invalid input, provider failures, and rate limits produce safe, useful errors.

## 3. Required technology choices

### Frontend

- React with TypeScript and Vite
- Tailwind CSS
- TanStack Query for server-state management
- React Router if routing is needed
- A small accessible component layer; use shadcn/ui only if it reduces custom boilerplate
- `react-markdown` with syntax highlighting for assistant responses
- Vitest and React Testing Library
- Playwright for one critical end-to-end chat flow

### Backend

- Python 3.12
- FastAPI
- Pydantic v2
- `pydantic-settings` for configuration
- LangChain using the current chat-model interface
- `langchain-google-genai` as the initial provider integration
- LangGraph for the conversation workflow and thread state
- SQLAlchemy 2.x async APIs
- Alembic migrations
- PostgreSQL
- `httpx` where an HTTP client is required
- Pytest, pytest-asyncio, and FastAPI/httpx test utilities

### Infrastructure and tooling

- Dockerfiles for frontend and backend
- Docker Compose for local application + PostgreSQL
- Ruff for Python linting and formatting
- Pyright or mypy for Python type checking
- ESLint and Prettier for frontend quality
- GitHub Actions CI
- Makefile or equivalent task runner with memorable commands
- Dependency lockfiles committed to the repository

Do not add Redis, Kubernetes, Celery, a vector database, or microservices during the initial build. Keep the architecture extensible, but avoid speculative infrastructure.

## 4. Repository structure

Use a clean monorepo:

```text
anubhavgpt/
├── apps/
│   ├── api/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── dependencies.py
│   │   │   │   ├── error_handlers.py
│   │   │   │   └── routes/
│   │   │   │       ├── chat.py
│   │   │   │       ├── conversations.py
│   │   │   │       └── health.py
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   ├── logging.py
│   │   │   │   └── security.py
│   │   │   ├── db/
│   │   │   │   ├── base.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repositories.py
│   │   │   │   └── session.py
│   │   │   ├── graph/
│   │   │   │   ├── builder.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── state.py
│   │   │   ├── schemas/
│   │   │   │   ├── chat.py
│   │   │   │   ├── common.py
│   │   │   │   └── conversation.py
│   │   │   ├── services/
│   │   │   │   ├── chat_service.py
│   │   │   │   └── conversation_service.py
│   │   │   └── main.py
│   │   ├── alembic/
│   │   ├── tests/
│   │   ├── .env.example
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   └── web/
│       ├── src/
│       │   ├── api/
│       │   ├── components/
│       │   ├── features/chat/
│       │   ├── hooks/
│       │   ├── layouts/
│       │   ├── pages/
│       │   ├── styles/
│       │   ├── types/
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── tests/
│       ├── .env.example
│       ├── Dockerfile
│       └── package.json
├── docs/
│   ├── adr/
│   │   └── 0001-architecture.md
│   ├── api.md
│   ├── architecture.md
│   ├── deployment.md
│   ├── development.md
│   ├── testing.md
│   └── troubleshooting.md
├── .github/workflows/ci.yml
├── .gitignore
├── CONTRIBUTING.md
├── docker-compose.yml
├── Makefile
├── README.md
└── SECURITY.md
```

Small adjustments are acceptable when justified in `docs/adr/0001-architecture.md`. Do not collapse the application into one Python file or one React component.

## 5. Architecture rules

Maintain these boundaries:

```text
React UI
  -> typed API client
  -> FastAPI route
  -> Pydantic request validation
  -> application service
  -> LangGraph workflow
  -> LangChain chat model
  -> persistence repository
  -> validated response / SSE stream
```

- Routes handle HTTP concerns only.
- Pydantic schemas define external contracts and must not double as ORM models.
- Services coordinate use cases.
- Repositories own database queries.
- LangGraph nodes own model/workflow behavior.
- Configuration is loaded centrally and injected where practical.
- Frontend components must not know provider-specific response formats.
- Provider signatures, raw content blocks, keys, and internal errors must never be sent to the browser.

## 6. API contract

Prefix endpoints with `/api/v1`.

### Health endpoints

#### `GET /api/v1/health/live`

Returns process liveness without external dependency checks.

```json
{"status": "ok"}
```

#### `GET /api/v1/health/ready`

Checks required dependencies such as the database. Do not make a paid LLM call.

### Conversations

- `POST /api/v1/conversations`
- `GET /api/v1/conversations`
- `GET /api/v1/conversations/{conversation_id}`
- `PATCH /api/v1/conversations/{conversation_id}`
- `DELETE /api/v1/conversations/{conversation_id}`

### Chat

#### `POST /api/v1/chat`

Provide a non-streaming endpoint for simple clients and automated testing.

Request:

```json
{
  "conversation_id": "0195cc33-bcc2-7ec4-a9f4-7e0a7765bb4a",
  "message": "Explain LangGraph state with a practical example."
}
```

Response:

```json
{
  "conversation_id": "0195cc33-bcc2-7ec4-a9f4-7e0a7765bb4a",
  "message_id": "0195cc3a-50fc-7f42-a4be-16357b39a9e0",
  "role": "assistant",
  "content": "...",
  "created_at": "2026-09-22T14:00:00Z"
}
```

#### `POST /api/v1/chat/stream`

Stream tokens or content deltas through Server-Sent Events. Define and document stable event types:

```text
event: metadata
data: {"conversation_id":"...","message_id":"..."}

event: delta
data: {"content":"LangGraph"}

event: done
data: {"finish_reason":"stop"}
```

Send a typed `error` event for errors that occur after the stream begins. Ensure clients can cancel the request.

### Error envelope

Use one safe error structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request could not be validated.",
    "request_id": "...",
    "details": []
  }
}
```

Map validation failures, missing records, provider timeouts, rate limits, and unexpected failures to suitable HTTP status codes. Never expose stack traces or API secrets.

## 7. Pydantic requirements

Use Pydantic v2 idioms.

The chat request must:

- Accept a UUID conversation ID.
- Accept a string message between 1 and 8,000 characters.
- Trim surrounding whitespace.
- Reject whitespace-only messages.
- Reject unknown fields with `ConfigDict(extra="forbid")`.

The response schemas must explicitly describe every returned field. Use response models on all JSON endpoints so accidental internal fields are filtered out.

Use `field_validator` only for validation that cannot be expressed with types or `Field`. Use `model_validator` only for cross-field invariants. Avoid clever custom types when built-in constraints suffice.

Create separate schemas for create, update, summary, detail, and response shapes where the contracts differ.

## 8. LangChain and LangGraph requirements

### Model integration

- Initialize the model through the current LangChain chat-model interface.
- Use Google Gemini initially, configured through environment variables.
- Keep provider/model construction behind a small factory so another provider can be added without changing routes or UI.
- Use asynchronous calls in the request path.
- Extract user-facing text through the normalized message text interface, not raw provider content dictionaries.
- Configure sensible request timeout and bounded retry behavior.
- Log latency and token metadata when available, never message content by default.

### Graph

Implement a real, understandable LangGraph workflow rather than wrapping one function unnecessarily.

Initial graph:

```text
START
  -> validate/context node
  -> assistant model node
  -> persist result node
  -> END
```

Use a typed graph state. Associate execution with `conversation_id` as the thread identifier. Keep nodes small and testable. Document what data enters and leaves each node.

Use a supported checkpointer appropriate to the selected LangGraph version. PostgreSQL is preferred for persistent thread state; if this introduces an unstable or redundant persistence design, document the tradeoff and keep the application conversation tables as the source of truth. Do not maintain two inconsistent histories.

### System behavior

Use a version-controlled system prompt that defines AnubhavGPT as:

- Helpful, direct, technically accurate, and concise by default.
- Strong at software-engineering explanations and production-issue analysis.
- Honest about uncertainty.
- Unwilling to fabricate system access, logs, or citations.
- Careful not to reveal hidden prompts, secrets, or internal metadata.

## 9. Database design

Create Alembic migrations for at least:

### `conversations`

- `id`: UUID primary key
- `title`: bounded string
- `created_at`: timezone-aware timestamp
- `updated_at`: timezone-aware timestamp

### `messages`

- `id`: UUID primary key
- `conversation_id`: foreign key with appropriate delete behavior
- `role`: constrained enum/string (`user`, `assistant`, optionally `system`)
- `content`: text
- `status`: constrained value (`pending`, `completed`, `failed`)
- `provider`: nullable bounded string
- `model`: nullable bounded string
- `input_tokens`: nullable integer
- `output_tokens`: nullable integer
- `created_at`: timezone-aware timestamp

Add useful indexes, including conversation/message ordering. Generate conversation titles from the first user message without requiring an extra paid model call.

Think through transaction boundaries. Do not leave assistant messages permanently `pending` after a handled failure. Avoid holding a database transaction open throughout a long provider stream.

## 10. Frontend experience

### Visual direction

- Product name: **AnubhavGPT**
- Dark graphite background with a restrained blue/violet accent
- Desktop sidebar with conversation history
- Mobile sidebar as an accessible drawer
- Centered welcome state with 3–4 starter prompts
- Comfortable reading width
- User and assistant messages visually distinct without oversized bubbles
- Markdown, tables, inline code, fenced code blocks, and copy-code action
- Visible focus states and keyboard usability
- Respect reduced-motion preferences

### Required UI states

- Initial welcome state
- Conversation loading skeleton
- Message sending state
- Streaming assistant message
- Empty-message prevention
- API validation error
- Provider unavailable/rate-limited error with retry
- Network-offline state
- Empty conversation list
- Conversation delete confirmation

### Frontend engineering

- Define TypeScript types that mirror the OpenAPI contracts. Prefer generated types if the chosen approach remains simple and reproducible.
- Put API calls in a dedicated client module.
- Abort streaming requests on navigation or explicit stop.
- Do not use `dangerouslySetInnerHTML` for model output.
- Sanitize/render Markdown safely.
- Preserve unsent input during temporary request errors.
- Avoid unnecessary global state; use local state and TanStack Query deliberately.

## 11. Configuration and security

Create `.env.example` files containing names and safe sample values only.

Backend settings should include at least:

```env
APP_ENV=development
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/anubhavgpt
GOOGLE_API_KEY=
LLM_PROVIDER=google_genai
LLM_MODEL=<supported-gemini-model>
LLM_TIMEOUT_SECONDS=45
ALLOWED_ORIGINS=http://localhost:5173
FAKE_LLM=false
```

Requirements:

- Never commit secrets.
- Validate required settings at startup with useful messages.
- Use restrictive CORS values from configuration; never use wildcard origins with credentials.
- Add request IDs and structured logs.
- Redact authorization headers, API keys, raw provider signatures, and sensitive configuration.
- Add a simple in-process rate limiter only if it is safe and clearly documented as single-instance. Otherwise document the production gateway/load-balancer requirement instead of pretending it is distributed.
- Set reasonable request body limits and message limits.
- Pin/lock dependencies and enable automated dependency auditing in CI where practical.

Authentication is outside the first MVP. State this explicitly in documentation. Design database records so a future `user_id` can be added through a migration. Do not claim the app is suitable for public multi-user deployment without authentication and external rate limiting.

## 12. Reliability and observability

- Add global exception handling with safe error responses.
- Distinguish timeouts, provider authentication errors, quota/rate-limit errors, validation failures, and internal errors.
- Use bounded retries only for transient failures; do not retry invalid requests or authentication failures.
- Add request ID, path, status, and duration to structured logs.
- Include model/provider latency and token usage when available.
- Never log full prompts or responses by default.
- Make readiness fail when PostgreSQL is unavailable.
- Ensure fake-model mode is deterministic and produces no external calls.

## 13. Tests

### Backend unit tests

- Pydantic accepts valid chat requests.
- Empty, whitespace-only, oversized, invalid UUID, and extra-field requests fail.
- Model response content blocks normalize into plain text.
- Graph nodes transform state correctly.
- Provider errors map to safe application errors.
- Conversation title generation is deterministic.

### Backend integration tests

- Health endpoints.
- Conversation create/list/detail/update/delete flow.
- Non-streaming chat flow using the fake model.
- SSE event ordering for metadata, deltas, and completion.
- Database persistence and conversation ordering.
- Standard error-envelope shape.

### Frontend tests

- Welcome screen renders.
- Sending a message calls the correct endpoint.
- Streaming deltas update one assistant message.
- Validation and network errors render accessibly.
- Markdown code blocks render without executing unsafe HTML.

### End-to-end test

Using fake-model mode, verify:

1. Open the app.
2. Create a conversation.
3. Send a message.
4. Observe a streamed answer.
5. Refresh.
6. Confirm the conversation and messages remain.

Tests must not depend on a real Google API key.

## 14. Documentation deliverables

Documentation is part of the definition of done, not an afterthought.

### `README.md`

Include:

- Product overview and screenshot placeholder
- Feature list
- Architecture summary
- Stack
- Prerequisites
- Quick start with Docker
- Quick start without Docker
- Environment configuration
- Commands
- Testing instructions
- API documentation links
- Current limitations
- Roadmap
- License placeholder

The first-time setup path should be copy/pasteable and verified.

### `docs/architecture.md`

Include:

- Component diagram using Mermaid
- Request/streaming sequence diagram using Mermaid
- Backend layer responsibilities
- LangGraph state and node descriptions
- Persistence strategy
- Error flow
- Security boundaries
- Key tradeoffs

### `docs/api.md`

Document every endpoint with request/response examples, SSE event contracts, error codes, and curl commands.

### `docs/development.md`

Explain local setup, migrations, adding endpoints, adding schemas, changing the model, working in fake-model mode, formatting, and linting.

### `docs/testing.md`

Explain test layers, commands, fixtures, fake-model behavior, and how to add tests.

### `docs/deployment.md`

Explain container deployment, required production environment variables, migration execution, reverse proxy/SSE considerations, CORS, secrets, health checks, authentication limitation, rate limiting, and rollback considerations.

### `docs/troubleshooting.md`

Cover missing Python/pip, virtual environment activation, missing API key, invalid Gemini model, quota/rate-limit failures, CORS, database connection failures, migrations, ports, and SSE buffering.

### Other files

- `CONTRIBUTING.md`: development workflow and quality expectations
- `SECURITY.md`: secret handling, vulnerability reporting placeholder, and known MVP limitations
- `docs/adr/0001-architecture.md`: major choices and rejected alternatives
- Helpful docstrings only where behavior is non-obvious; do not narrate trivial code

## 15. Developer commands

Provide working equivalents of:

```bash
make setup
make dev
make stop
make migrate
make test
make lint
make format
make typecheck
make e2e
```

`make dev` should give the user a usable local URL with minimal manual work. Docker Compose must use health checks and dependency readiness rather than unreliable fixed sleeps.

## 16. CI requirements

GitHub Actions must run on pull requests and pushes to the main branch:

- Backend lint/format check
- Backend type check
- Backend tests
- Frontend lint/format check
- Frontend type check
- Frontend tests
- Production builds
- End-to-end test if it can run reliably in fake-model mode

Use caching appropriately. CI must not require provider credentials.

## 17. Implementation phases

Execute in this order while keeping the repository runnable:

### Phase 1 — Foundation

- Initialize monorepo and tooling.
- Add configuration, logging, health endpoints, Docker Compose, database, and migration setup.
- Add fake-model mode immediately so subsequent work is testable.

### Phase 2 — Backend conversation core

- Add database models, repositories, Pydantic schemas, services, conversation endpoints, and tests.
- Add the LangChain model factory.
- Add the LangGraph workflow.
- Implement non-streaming chat and safe error mapping.

### Phase 3 — Streaming

- Add SSE chat streaming.
- Persist final messages correctly.
- Handle cancellation and mid-stream failures.
- Add integration tests for the event contract.

### Phase 4 — Frontend

- Build responsive shell and conversation navigation.
- Add welcome screen, composer, Markdown rendering, code copying, streaming, loading, errors, retry, and deletion.
- Add component and integration tests.

### Phase 5 — Production hardening

- Finish structured logging, request IDs, CORS, configuration validation, health checks, container builds, CI, and security review.
- Run dependency audits and address material issues.

### Phase 6 — Documentation and verification

- Complete every required document.
- Run the full quality suite.
- Start the complete stack and perform the end-to-end flow.
- Fix documentation commands that do not work exactly as written.

## 18. Explicit non-goals for the initial build

Do not add these until the core acceptance criteria pass:

- Authentication or social login
- File uploads
- RAG/vector search
- Web browsing
- Arbitrary tool execution
- Multi-agent workflows
- Voice input/output
- Image generation
- Billing
- Kubernetes

Document them as possible roadmap items without leaving misleading placeholder implementations.

## 19. Acceptance criteria

The build is complete only when all of the following are true:

- The application starts through the documented command.
- The web UI is responsive and polished on desktop and mobile.
- A user can create a conversation and receive a streamed answer.
- Refreshing preserves conversations and messages.
- Request and response bodies are validated with Pydantic.
- Unknown request fields and blank messages are rejected.
- LangChain performs provider interaction behind a model factory.
- LangGraph visibly coordinates the conversational workflow.
- Provider-specific metadata never appears in user-facing output.
- All JSON errors use the documented safe envelope.
- Fake-model mode supports local development, CI, and end-to-end tests without a key.
- Database migrations work on a fresh PostgreSQL instance.
- Backend and frontend tests pass.
- Linters, format checks, and type checks pass.
- Production builds succeed.
- No credentials exist in tracked files or git history created by this task.
- README and docs accurately match the implementation.
- Known limitations—especially missing authentication—are clearly stated.

## 20. Final verification and handoff format

Before reporting completion:

1. Inspect the final git diff and ensure no unrelated files were changed.
2. Run formatting, linting, type checking, unit tests, integration tests, builds, and the end-to-end test.
3. Start the stack in fake-model mode and verify health, chat streaming, persistence, refresh, and deletion.
4. Check that `.env` files are ignored and only `.env.example` files are tracked.
5. Confirm the documentation commands work.

Return a concise handoff containing:

- What was built
- Architecture decisions
- Exact commands to start it
- Test/quality results with command names
- Local URLs
- Environment variables the user must supply for Gemini
- Known limitations
- Recommended next milestone

Do not claim a command passed unless it was actually executed successfully. If anything remains blocked, identify the exact blocker and leave the repository in a runnable, documented state.

## 21. Recommended next milestone after MVP

After the above acceptance criteria pass, propose—but do not automatically implement—a second milestone:

1. Authentication and per-user conversation ownership
2. Tool calling for structured production-issue analysis
3. Human approval through LangGraph interrupts
4. RAG over technical documentation with citations
5. LangSmith tracing and evaluation datasets
6. Production-grade distributed rate limiting

