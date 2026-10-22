# Testing and verification

[Documentation hub](README.md) · [Evidence](EVIDENCE.md) · [Workflow](../.github/workflows/ci-cd.yml)

## Verified application baseline

Source [`8944da7`](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574) passed the complete enabled pipeline on 22 October 2026. [Original PostgreSQL output](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/pytest-postgres.txt): **44 passed, 97.67% coverage**. Compose and kind ingress each passed four desktop/mobile scenarios. The backend coverage gate is 80%.

Earlier SQLite-only results and older green runs remain dated historical evidence. They do not replace the PostgreSQL concurrency result or a later source's own run.

## Backend checks

From the repository root, with Python 3.12 available:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install --require-hashes -r backend/requirements-dev.txt
ruff check backend scripts
ruff format --check backend scripts
cd backend
pytest -v --cov=app --cov-report=term-missing --cov-report=xml
```

Without `TEST_DATABASE_URL`, each test uses a temporary SQLite database. The PostgreSQL-only concurrency test skips explicitly. `DATABASE_URL` is not selected as the test data source.

For PostgreSQL parity, provide a dedicated disposable database whose name ends in `_test`, set `TEST_DATABASE_URL` to its `postgresql+psycopg://` URL using private credentials, and run the same suite. The fixture removes test rows and rejects a non-SQLite database without that suffix. The application's default Compose PostgreSQL port is not exposed to the host; CI supplies its own disposable PostgreSQL service.

With the virtual environment active, from `backend/`, the CI migration checks are:

```bash
export DATABASE_URL="$TEST_DATABASE_URL"
alembic upgrade head
alembic check
alembic downgrade base
alembic upgrade head
pytest -v --cov=app --cov-report=term-missing
```

Only use that downgrade sequence on the disposable test database. [Tests and fixtures](../backend/tests/) cover CRUD, validation, duplicate-SKU rollback, stock bounds, retained history, pagination, statistics, readiness/error handling, metrics, seed idempotency and migration consistency. PostgreSQL racing removals verify one success and one 409 instead of a negative balance.

## Frontend and browser checks

From the repository root, with Node 24 matching CI:

```bash
npm --prefix frontend ci --ignore-scripts
npm --prefix frontend run lint
npm --prefix frontend test
npm --prefix frontend run build
```

Four frontend utility tests cover threshold boundaries, CSV escaping/formula handling, error messages and empty 204 responses. For Playwright, start the local Compose application first, then:

```bash
npm --prefix e2e ci
cd e2e
npx playwright install --with-deps chromium
BASE_URL=http://localhost:3000 npm test
```

Desktop/mobile projects exercise create, inspect, edit, stock adjustment, excessive-removal rejection, retained ledger, search/filter/export/navigation and page-overflow checks. Captures come from the running app.

## Container and cluster checks

| Gate | Actual verification |
|---|---|
| Compose | Config, migrations, health, HTTP CRUD, non-root IDs and four browser scenarios |
| Persistence | Synthetic product/ledger retained after a real PostgreSQL container restart |
| Infrastructure | Locked Terraform init/validate/mock topology tests and Helm schema/wiring |
| Kind | Exact scanned images, Ready replicas, Services, Traefik ingress, HPA metrics and browser tests |
| Monitoring | UP targets, positive live request query and authenticated populated Grafana |
| Troubleshooting | Isolated wrong-selector and missing-image faults diagnosed, repaired and verified |
| Flux | Tested Git SHA fetched; release revision 2 and running configuration change observed |
| Cleanup helper | Ten scope/absence checks, including rejecting AccessDenied as proof of deletion |

Run `python3 scripts/verify-cleanup-scope.py` to reproduce the helper's non-cloud unit checks. Terraform mocks are not AWS provisioning proof. The separate [real AWS lifecycle](AWS-EKS-RUNTIME-VERIFICATION.md) and [approved teardown](AWS-CLEANUP-VERIFICATION.md) have their own user-executed evidence.

Local Docker/container execution depends on your machine. This documentation-only polish uses static/media checks and the existing GitHub Actions regression; it does not claim a locally executed Docker run. [Full original run manifest](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ci-run.json).
