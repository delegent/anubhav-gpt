FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app/apps/api
COPY apps/api/pyproject.toml ./apps/api/pyproject.toml
COPY apps/api/app ./apps/api/app
RUN pip install --no-cache-dir -e "./apps/api[dev]"
COPY . .
WORKDIR /app/apps/api
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
