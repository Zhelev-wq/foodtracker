FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y curl
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /code
COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
HEALTHCHECK --interval=5m --timeout=30s --start-period=30s --retries=3 CMD [ "curl", "-f", "http://localhost:8000/health" ]
