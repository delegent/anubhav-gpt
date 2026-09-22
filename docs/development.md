# Development

Run `make setup` once, then `make dev` for the full Docker stack.

The backend settings live in `apps/api/app/core/config.py`. Use `apps/api/.env.example` and keep real `.env` files untracked. Fake-model mode is enabled with `FAKE_LLM=true` and makes no external calls.

Add endpoints by creating a schema, service method, repository method if persistence is needed, and a thin route under `apps/api/app/api/routes`.

Change the model in the environment with `LLM_PROVIDER`, `LLM_MODEL`, and `GOOGLE_API_KEY`. Provider construction stays in `apps/api/app/graph/nodes.py`.

Run migrations with `make migrate`. Create future migrations under `apps/api/alembic/versions`.

Quality commands: `make format`, `make lint`, `make typecheck`, `make test`.
