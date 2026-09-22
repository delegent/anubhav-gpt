# Architecture

```mermaid
flowchart LR
  UI[React UI] --> Client[Typed API client]
  Client --> Route[FastAPI route]
  Route --> Schema[Pydantic validation]
  Schema --> Service[Application service]
  Service --> Graph[LangGraph workflow]
  Graph --> Model[LangChain chat model]
  Service --> Repo[Repository]
  Repo --> DB[(PostgreSQL)]
```

```mermaid
sequenceDiagram
  participant Browser
  participant API
  participant Graph
  participant Model
  participant DB
  Browser->>API: POST /api/v1/chat/stream
  API->>DB: persist user message
  API-->>Browser: metadata event
  API->>Model: async stream
  Model-->>API: content chunks
  API-->>Browser: delta events
  API->>DB: persist assistant message
  API-->>Browser: done event
```

Routes handle HTTP details only. Schemas define external contracts. Services coordinate use cases. Repositories own SQLAlchemy queries. LangGraph nodes validate context, call the assistant model, and return persistable state.

The app uses conversation tables as the source of truth. LangGraph receives `thread_id=conversation_id`; a separate checkpointer is not used in the MVP to avoid two divergent histories.

Errors pass through one safe envelope and provider internals are not returned to the browser. CORS is configured from settings. Authentication and distributed rate limiting are production requirements outside this MVP.
