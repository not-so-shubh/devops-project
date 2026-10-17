# Testing and verification

Local verification at implementation time: 43 backend tests passed, one PostgreSQL-only concurrency test skipped, 98.83% statement coverage (257 statements, three uncovered). All API route logic was exercised. The uncovered code was the default database dependency (replaced in tests) and CLI-only seed printing. Coverage includes the idempotent seed logic. See [pytest-local.txt](evidence/pytest-local.txt).

The actual PostgreSQL GitHub quality job subsequently passed all 44 tests, including concurrency, with 97.67% coverage. See [github-quality.txt](evidence/github-quality.txt).

Tests cover root/docs, liveness/readiness, sanitized DB failures, Prometheus exposition and bounded route labels, product CRUD, duplicate SKU rollback, validation, missing records, search/status/category/pagination, opening balances, increments/decrements, insufficient stock, upper limits, stock statistics/trends, empty data, movement history, retained audit after deletion, independent-session persistence, seed idempotency and reversible migrations/model consistency.

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install --require-hashes -r backend/requirements-dev.txt
cd backend
pytest -v --cov=app --cov-report=term-missing --cov-report=xml
ruff check .
ruff format --check .
```

Without `TEST_DATABASE_URL`, every test gets its own temporary SQLite database. `DATABASE_URL` is never selected as the test database. To reproduce the PostgreSQL CI tests, provision a dedicated empty database whose name ends in `_test`, then:

```bash
export TEST_DATABASE_URL='postgresql+psycopg://stockpilot:YOUR_PASSWORD@localhost:5432/stockpilot_test'
export DATABASE_URL="$TEST_DATABASE_URL"
alembic upgrade head
alembic check
alembic downgrade base
alembic upgrade head
pytest -v --cov=app --cov-report=term-missing
```

The fixture deletes test rows, so never point it at business data. It rejects a non-SQLite database name without `_test`. PostgreSQL runs two simultaneous removals of eight units from a balance of twelve; exactly one must return 201 and the other 409, leaving four units. SQLite skips that concurrency claim rather than pretending its locking is PostgreSQL behavior.

Frontend validation:

```bash
cd frontend
npm ci --ignore-scripts
npm run lint
npm test
npm run build
```

Four utility tests check threshold boundaries, CSV quote/formula handling, server validation error presentation, and 204 deletion behavior. Playwright adds real browser acceptance against an already running stack:

```bash
cd e2e
npm ci
npx playwright install --with-deps chromium
npm test
```

Desktop and mobile projects verify create, inspect, edit, reject excessive removal, adjust stock, observe low-stock status, delete, inspect retained movements via UI and API, search empty states, filters, CSV download, dialogs/navigation and absence of page overflow. Screenshots are captured from the running application, not a design mockup.

The CI Compose job uses actual PostgreSQL, non-root images, Nginx proxying, Alembic and named storage. The separate kind job loads the exact scanned images, installs real Ingress and monitoring, deploys Helm, checks rollouts and resource metrics, tests UI through Ingress, and requires an UP scrape target and non-zero Prometheus request rate. It is a real disposable Kubernetes environment, not proof of AWS/EKS provisioning.

Local runtime limitations are retained in evidence: Docker daemon access is denied, kubectl has no cluster, and Terraform provider execution/checksum validation is restricted here despite successful initialization. CI results take precedence only for the commands that actually passed there. Review the evidence index for the latest outcome.
