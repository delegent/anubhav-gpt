# ADR 0001: MVP Architecture

## Status

Accepted.

## Decision

Use a monorepo with `apps/api` and `apps/web`. Keep FastAPI routes thin, use Pydantic for contracts, SQLAlchemy repositories for persistence, services for use cases, and LangGraph for the assistant workflow.

The MVP uses PostgreSQL in Docker and SQLite for isolated tests. Conversation tables are the source of truth; LangGraph gets a thread identifier but no independent persistent checkpointer yet.

## Rejected Alternatives

- Redis, Celery, Kubernetes, vector databases, and tool execution were rejected as speculative for the first milestone.
- A single Python file or single React component was rejected because it obscures ownership boundaries.
- A second LangGraph persistence store was deferred because it can create inconsistent histories without a clear need.
