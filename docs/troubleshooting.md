# Troubleshooting

- Missing Python or pip: install Python 3.12 and rerun `make setup`.
- Missing Node: install Node 22 or use Docker.
- Missing API key: keep `FAKE_LLM=true` or set `GOOGLE_API_KEY`.
- Invalid Gemini model: update `LLM_MODEL` to a currently supported Gemini chat model.
- Quota or rate limit: fake mode should still work; production should surface `PROVIDER_ERROR`.
- CORS: ensure `ALLOWED_ORIGINS` includes the web origin.
- Database failures: check `DATABASE_URL`, Postgres health, and `make migrate`.
- Ports in use: stop conflicting services or edit Compose port mappings.
- SSE buffering: disable proxy buffering for `/api/v1/chat/stream`.
