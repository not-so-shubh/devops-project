# Application deliverable

[Documentation hub](../docs/README.md) · [Run StockPilot](../README.md#quick-start)

This directory maps the coursework's `application/` deliverable to the canonical [`backend/`](../backend/README.md) and [`frontend/`](../frontend/README.md) sources. There is one implementation, with no duplicate application tree.

StockPilot provides product CRUD, unique SKUs, atomic signed stock adjustments, retained movement history and database-backed statistics. FastAPI/SQLAlchemy/Alembic use PostgreSQL; React uses relative `/api` routes. [Architecture](../docs/ARCHITECTURE.md) · [Tests](../docs/TESTING.md) · [Actual captures](../docs/EVIDENCE.md).

Use the root quick start to generate private local credentials and start Compose. Open localhost:3000. Optional `python -m app.seed` runs inside the backend container and is idempotent.
