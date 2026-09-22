# Deployment

Build containers with Docker Compose or your platform builder. Run Alembic migrations before routing production traffic.

Required production environment variables include `DATABASE_URL`, `ALLOWED_ORIGINS`, `FAKE_LLM=false`, `LLM_PROVIDER=google_genai`, `LLM_MODEL`, and `GOOGLE_API_KEY`.

Put the API behind a reverse proxy that does not buffer SSE responses. Configure health checks against `/api/v1/health/live` and readiness checks against `/api/v1/health/ready`.

This MVP has no authentication and no distributed rate limiter. Add auth, per-user conversation ownership, gateway rate limiting, and secret management before public multi-user deployment.

Rollback by redeploying the previous image and ensuring database migrations are backwards compatible.
