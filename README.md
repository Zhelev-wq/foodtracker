# FoodTracker

A nutrition tracking app. You log meals and it records the macros plus a full
micronutrient breakdown for each food: vitamins, minerals, and the individual fat types,
all per 100g. You can add your own foods and save recipes so you don't re-enter the same
ingredients every day.

I built it to work with async Python on the backend and a React frontend. This a personal project and still in progress, but the core works and runs. The primary goal of this project is to create the right environment for me to learn different technologies rather than creating a commercial app.

## Stack

**Backend.** FastAPI, SQLAlchemy 2.0 (async, on asyncpg), PostgreSQL, Alembic for
migrations, Pydantic v2, JWT auth. Python 3.13, dependencies managed with uv.

**Frontend.** React 19 with TypeScript, Vite, Tailwind, MUI. The API client types are
generated from the backend's OpenAPI schema, so the two stay in sync.

**Infra.** Docker Compose brings up Postgres, runs the migrations, and starts the API and
the frontend.

## Design notes

- **Async throughout.** FastAPI, the async SQLAlchemy session, and asyncpg. The database
  calls don't block the event loop.

- **Fuzzy food search.** People type food names with typos, so exact matching fails
  often. Search uses Postgres `pg_trgm` trigram matching with a GIN index on the name
  column, ordered by similarity. A search for "chikn brest" returns chicken breast.

- **Shared and custom foods.** The food table holds common foods with no owner alongside
  custom foods owned by a user. Search returns both, scoped so a user only sees the
  shared set and their own foods.

- **Micronutrients.** Each food can hold a vitamin profile, a mineral profile, and a fat
  breakdown. Each one lives in its own table with a one-to-one link to the food, keyed
  per 100g.

- **Shared model for entries and recipes.** A logged meal and a saved recipe have the
  same shape: a named record that owns a list of food-and-grams items. They inherit from
  shared abstract SQLAlchemy base classes instead of duplicating the structure.

- **Auth.** JWT bearer tokens over the OAuth2 password flow, passwords hashed with argon2.
  Token checks require the expiry and subject claims. A bad or missing token returns a
  generic 401, so responses don't reveal whether an account exists.

- **Separate input and output schemas.** Request and response models are different
  Pydantic classes, so internal fields stay out of responses.

## Tests

The tests run against a real PostgreSQL instance, because the app depends on
Postgres-only features. The trigram search and its GIN index don't exist in SQLite, so
testing on SQLite would skip the parts worth testing. Testcontainers starts a temporary
Postgres (with `pg_trgm` enabled) for each run.

Each test runs inside a transaction that gets rolled back afterward, so tests stay
isolated and don't depend on run order. Coverage includes the auth flow and the CRUD
paths for foods, entries, recipes, and their items.

```bash
uv run pytest
```

## Running it

### With Docker

You need Docker and a `.env` file. Copy the sample and fill it in:

```bash
cp .env.sample .env
```

The variables:

| Variable       | What it's for                               |
| -------------- | ------------------------------------------- |
| `DB_NAME`      | Postgres database name                      |
| `USERNAME`     | Postgres user                               |
| `PASSWORD`     | Postgres password                           |
| `HOST_ADDRESS` | DB host (`db` when running under Compose)   |
| `PORT`         | DB port (`5432`)                            |
| `DB`           | driver/name used to build the connection    |
| `SECRET_KEY`   | signing key for JWTs                         |

Generate a real secret key:

```bash
openssl rand -hex 32
```

Then start it:

```bash
docker compose up --build
```

Compose starts Postgres, waits for its healthcheck, runs the Alembic migrations, then
starts the API and the frontend. Open [http://localhost:8080](http://localhost:8080).
nginx serves the frontend there and proxies API calls under `/api` to the backend. The
backend port isn't published to the host, so `localhost:8000` won't respond in the Docker
setup. That address and the `/docs` page only work in the local-dev path below.

### Locally, for development

Backend:

```bash
uv sync
uv run alembic upgrade head
uv run fastapi dev
```

This serves the API on [http://localhost:8000](http://localhost:8000), with interactive
docs at [http://localhost:8000/docs](http://localhost:8000/docs).

Frontend:

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server runs on port 5173, which the API already allows through CORS. 

Demo database with sample foods is planned for a later date.

## Layout

```
app/
  api/          route handlers: foods, food entries, entry items, recipes, users
  db/           SQLAlchemy models and the async engine/session setup
  validators/   Pydantic schemas, split into input and output models
  auth.py       JWT, password hashing, the current-user dependency
  main.py       app wiring, routers, CORS, health check
alembic/        migrations
tests/          pytest suite (Testcontainers)
frontend/       React + TypeScript app
```

## API

Everything sits under `/api`:

- `/api/users` — registration, token login, current user
- `/api/foods` — search the food library, create and edit your own foods
- `/api/food-entries` — log meals
- `/api/food-entry-items` — the individual foods inside an entry
- `/api/recipes` — build reusable food groups and log them as entries

There's a `/health` endpoint that the container healthcheck hits.

## How this was built

I wrote this codebase by hand. Every line and every design decision is mine. I used AI
as a research tool for reading documentation and weighing options. It didn't write code.
Ask me why any part of this works the way it does and I can tell you.

## Where it's going

Two things are missing. There's no CI yet, and it isn't deployed anywhere public. Next
are a GitHub Actions workflow to run the tests on each push, and a cloud deployment so
there's a live demo.
