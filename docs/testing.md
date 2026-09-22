# Testing

Backend tests use pytest, httpx ASGI transport, SQLite in memory, and fake-model mode. They cover schema validation, graph helpers, health, conversations, non-streaming chat, SSE event order, and the standard error envelope.

Frontend tests use Vitest and React Testing Library. Playwright contains the first e2e smoke flow and is intended to grow with the app.

Commands:

```bash
make test
make e2e
```

Tests must not require `GOOGLE_API_KEY`.
