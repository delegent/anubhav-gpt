.PHONY: setup dev stop migrate test lint format typecheck e2e

setup:
	cd apps/api && python -m pip install -e ".[dev]"
	cd apps/web && npm install

dev:
	docker compose up --build

stop:
	docker compose down

migrate:
	alembic -c apps/api/alembic.ini upgrade head

test:
	cd apps/api && pytest
	cd apps/web && npm test

lint:
	cd apps/api && ruff check .
	cd apps/web && npm run lint

format:
	cd apps/api && ruff format . && ruff check --fix .
	cd apps/web && npm run format

typecheck:
	cd apps/api && mypy app
	cd apps/web && npm run build

e2e:
	cd apps/web && npm run e2e
