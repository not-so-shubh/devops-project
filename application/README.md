# Application deliverable

The application source is maintained in [`backend/`](../backend/) and [`frontend/`](../frontend/) to match the session's graded layout. This directory maps the homework PDF's `application/` entry to those canonical sources without maintaining duplicate implementations.

StockPilot is an original inventory application: product CRUD, atomic stock adjustments, retained movement ledger and live inventory statistics. FastAPI/SQLAlchemy/Alembic use PostgreSQL; React calls relative `/api` endpoints. See [API/setup](../README.md), [tests](../docs/TESTING.md) and [actual app captures](../docs/EVIDENCE.md).

From the repository root: copy `.env.example` to `.env`, set your local password, run `docker compose up --build -d --wait`, then optionally `docker compose exec backend python -m app.seed`. Open http://localhost:3000.
