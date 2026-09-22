# API

Base path: `/api/v1`.

## Health

```bash
curl http://localhost:8000/api/v1/health/live
curl http://localhost:8000/api/v1/health/ready
```

Response:

```json
{"status":"ok"}
```

## Conversations

Create:

```bash
curl -X POST http://localhost:8000/api/v1/conversations \
  -H 'content-type: application/json' \
  -d '{"title":"New conversation"}'
```

List, detail, rename, delete:

```bash
curl http://localhost:8000/api/v1/conversations
curl http://localhost:8000/api/v1/conversations/{id}
curl -X PATCH http://localhost:8000/api/v1/conversations/{id} -H 'content-type: application/json' -d '{"title":"Incident review"}'
curl -X DELETE http://localhost:8000/api/v1/conversations/{id}
```

## Chat

Non-streaming:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H 'content-type: application/json' \
  -d '{"conversation_id":"00000000-0000-0000-0000-000000000000","message":"Explain LangGraph state."}'
```

Streaming:

```bash
curl -N -X POST http://localhost:8000/api/v1/chat/stream \
  -H 'content-type: application/json' \
  -d '{"conversation_id":"00000000-0000-0000-0000-000000000000","message":"Explain LangGraph state."}'
```

SSE event order is `metadata`, one or more `delta` events, then `done`. After a started stream fails, the API emits `error`.

## Error Envelope

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request could not be validated.",
    "request_id": "uuid",
    "details": []
  }
}
```

Common codes: `VALIDATION_ERROR`, `NOT_FOUND`, `PROVIDER_ERROR`, `INTERNAL_ERROR`.
