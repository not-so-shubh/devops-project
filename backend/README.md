# Backend

[Documentation hub](../docs/README.md) · [Architecture](../docs/ARCHITECTURE.md) · [Testing](../docs/TESTING.md)

FastAPI exposes validated inventory APIs. SQLAlchemy/Psycopg access PostgreSQL; Alembic owns the deployed schema. Source lives in [`app/`](app/), migrations in [`alembic/`](alembic/), and tests in [`tests/`](tests/).

## Local development

The root [Compose quick start](../README.md#quick-start) is the shortest full-stack path. For host development, use Python 3.12 and a separately available PostgreSQL database; default Compose PostgreSQL is not published to a host port.

From the repository root:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install --require-hashes -r backend/requirements-dev.txt
cd backend
```

Set a private `DATABASE_URL` such as `postgresql+psycopg://USER:ENCODED_PASSWORD@HOST:5432/stockpilot` using your own credentials, then:

```bash
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

The seed is optional/idempotent. Open localhost:8000/docs. The app does not create tables during startup. `/health` is liveness; `/ready` verifies database connectivity and migrated schema; `/metrics` is Prometheus exposition.

## API contracts

| Method | Route | Behavior |
|---|---|---|
| GET | `/api/products` | `search`, `status=all/healthy/low/out`, `category`, `offset`, `limit` |
| POST | `/api/products` | Create details and optional opening stock atomically; 201 |
| GET / PUT / DELETE | `/api/products/{id}` | Read, replace details, or delete catalog record; ledger retained |
| POST | `/api/inventory/adjustments` | `product_id`, signed nonzero `quantity_change`, explanatory `reason` |
| GET | `/api/inventory/movements` | Latest-first movements; optional product filter and pagination |
| GET | `/api/inventory/stats` | Product/unit/value/reorder counts, categories and seven-day movement trend |

Product details include `sku`, `name`, `category`, `selling_price`, `reorder_threshold` and `description`; creation also accepts `stock_quantity`. Quantity changes use adjustments. SKU normalization is uppercase, input rejects unknown fields, money uses Decimal, and quantity bounds are enforced in validation and the database.

Stock updates and movement insertion commit in one transaction. Conditional SQL prevents negative stock under concurrent removals. Nullable product references plus SKU/name snapshots retain history after deletion. Errors distinguish validation (422), missing records (404), conflicts (409) and sanitized database unavailability (503).

## Tests and runtime

From `backend/` with the virtual environment active: `pytest -v --cov=app --cov-report=term-missing`. Temporary SQLite is convenient locally; a separate PostgreSQL `TEST_DATABASE_URL` ending in `_test` exercises concurrency. Never point the destructive fixture at business data. [Verified PostgreSQL result](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/pytest-postgres.txt): 44 passed, 97.67% coverage.

The [Dockerfile](Dockerfile) runs one Uvicorn worker as UID 10001 on 8000; replicas provide capacity and keep per-process metrics clear. The capstone has no application authentication/RBAC. See [operational tradeoffs](../docs/ARCHITECTURE.md#operational-tradeoffs).
