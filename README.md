# StockPilot

**Inventory, under control.** StockPilot is an original inventory operations platform for small businesses. It combines a responsive React workspace with a FastAPI API, PostgreSQL persistence, and a stock ledger that keeps the history after a product leaves the catalog.

[CI/CD](https://github.com/not-so-shubh/devops-project/actions/workflows/ci-cd.yml) · [Evidence](docs/EVIDENCE.md) · [Rubric audit](docs/RUBRIC-CHECKLIST.md) · [Demo script](docs/FINAL-DEMO-SCRIPT.md)

## Verified submission status

[Complete successful CI/CD run](https://github.com/not-so-shubh/devops-project/actions/runs/39056922560) · [Actual screenshots and reports](docs/EVIDENCE.md) · [Final submission actions](docs/SUBMISSION.md)

The reviewed source `54513c248b2b2cb0b6bb2a0a41c7cc4a03b9b69c` passed PostgreSQL tests, Compose/browser checks, both image scans and GHCR publication, Helm/Ingress/HPA, populated Grafana, troubleshooting repairs and real Flux reconciliation. The evidence-based audit covers 39 of 46 criteria (83 rubric points); these are verified criteria, not awarded marks. A real AWS plan/VPC/EKS/destroy cycle and the student's security explanation/presentation remain required. Official form submission is **Student action — excluded from this task**. Evidence is pinned to that tested revision; newer commits need their own successful run.

## Screenshots

![StockPilot running in the actual desktop browser test](https://raw.githubusercontent.com/not-so-shubh/devops-project/fb09b2543f7335779c7c32289123be69f52c5e66/docs/evidence/frontend-desktop.png)

[Mobile view](https://github.com/not-so-shubh/devops-project/blob/fb09b2543f7335779c7c32289123be69f52c5e66/docs/evidence/frontend-mobile.png) · [Prometheus: two targets UP](https://github.com/not-so-shubh/devops-project/blob/fb09b2543f7335779c7c32289123be69f52c5e66/docs/evidence/prometheus-targets.png) · [Grafana: populated live dashboard](https://github.com/not-so-shubh/devops-project/blob/fb09b2543f7335779c7c32289123be69f52c5e66/docs/evidence/grafana-dashboard.png)

## What you can do

- See product count, total units, selling-price inventory value, reorder alerts, and seven days of real stock movements.
- Create, inspect, search, filter, edit, and delete products with unique SKUs, categories, prices, descriptions, and reorder thresholds.
- Receive or remove stock with an explanatory reason. Conditional database updates prevent concurrent removals from overselling.
- Review the retained, paginated stock ledger, including opening balances and products that have been deleted.
- Use desktop and mobile navigation, accessible focus-trapped dialogs, loading/error/empty states, notifications, and a formula-safe CSV export.

No chart or activity entry is hardcoded in the frontend. Optional seed data is inserted explicitly into the database, never at application startup. Prices and the dashboard use INR; inventory value is stock × selling price, not an accounting cost valuation. Low-stock KPI includes out-of-stock products; the table's Low stock filter shows positive balances at/below threshold, and Out of stock shows zero.

## Architecture

```mermaid
flowchart TD
  Dev[Developer commit] --> CI[GitHub Actions]
  CI --> Quality[PostgreSQL tests and browser acceptance]
  Quality --> Scan[Build and Trivy gate]
  Scan --> Registry[GHCR images with commit SHA]
  Scan --> Kind[Disposable Kubernetes validation]
  Registry --> EKS[EKS after explicit AWS approval]
  Kind --> Helm[Helm release]
  EKS --> Helm
  Helm --> Ingress[Traefik Ingress]
  Ingress --> UI[React and Nginx]
  Ingress --> API[FastAPI]
  UI --> API
  API --> PG[PostgreSQL and Alembic]
  API --> Prom[Prometheus]
  Prom --> Grafana[Grafana]
```

Local browser calls use relative `/api` URLs. Compose Nginx preserves the prefix when proxying to `backend:8000`. Cluster Ingress routes `/api` directly to that same backend Service, and `/` to frontend port 8080. There are no rewrite annotations or mismatched ports. Traefik is used because ingress-nginx retired in March 2026; see [the Kubernetes announcement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/).

## Stack and layout

React 19 + Vite 8, modern CSS and Lucide; Python 3.12 + FastAPI, SQLAlchemy, Pydantic, Psycopg, Alembic; PostgreSQL 17; Pytest, Ruff, Playwright; Docker/Compose; GitHub Actions, Trivy and GHCR; Terraform AWS provider 6.69; EKS 1.35; Helm, Traefik, HPA, Prometheus Operator and Grafana. Python dependencies have exact versions and hashes, npm dependencies have lockfiles, Actions use commit pins, and container bases use registry digests. See [architecture decisions](docs/ARCHITECTURE.md).

| Path | Purpose |
|---|---|
| `application/`, `docker/`, `kubernetes/` | PDF deliverable guides pointing to the canonical source/build/chart files |
| `backend/app/` | API, validated contracts, database models and explicit seed command |
| `backend/alembic/` | Reversible schema migration; no production `create_all` |
| `backend/tests/`, `e2e/` | Isolated database tests and desktop/mobile acceptance |
| `frontend/` | Original dashboard and non-root Nginx image |
| `.github/workflows/ci-cd.yml` | Quality, infrastructure, Compose, scan, publish, kind and optional EKS |
| `terraform/` | Two-AZ VPC, public/private subnets, NAT, EKS, workers and OIDC access |
| `helm/stockpilot/`, `k8s/` | Application chart, namespace and EBS storage class |
| `monitoring/` | Prometheus, Grafana dashboard, ingress and metrics-server values |
| `scripts/`, `troubleshooting/` | Checks, secret bootstrap, traffic generation and isolated exercises |
| `docs/` | Deployment, testing, demonstration, rubric and evidence |

## Run the complete stack

Prerequisites: Git, Docker Engine/Desktop and Compose v2.20+ (v2.39.4 config was checked). Allocate at least 4 GB to Docker. Ports 3000 and 8000 must be free.

```bash
git clone https://github.com/not-so-shubh/devops-project.git
cd devops-project
cp .env.example .env
# Replace the local development password with a long URL-safe value.
docker compose config --quiet
docker compose up --build -d --wait --wait-timeout 180
docker compose exec backend python -m app.seed   # optional, idempotent
docker compose ps
python3 scripts/smoke.py
```

Open [StockPilot](http://localhost:3000), [Swagger](http://localhost:8000/docs), [readiness](http://localhost:8000/ready), and [metrics](http://localhost:8000/metrics). `.env` is ignored. PostgreSQL is private to the Compose network, with a named persistent volume; both published application ports bind only to loopback.

```bash
docker compose logs -f backend
docker compose exec postgres psql -U stockpilot -d stockpilot -c 'SELECT sku, stock_quantity FROM products;'
docker compose stop
docker compose up -d --wait           # preserves database
# Stop the stack; retain its data:
docker compose down
# Explicitly delete local demonstration data only when finished:
docker compose down -v
```

## Configuration and migrations

| Variable/config | Where | Meaning |
|---|---|---|
| `POSTGRES_DB`, `POSTGRES_USER` | Compose `.env` | Default `stockpilot` |
| `POSTGRES_PASSWORD` | Compose `.env` | Required; use a URL-safe random password because Compose embeds it in a URL |
| `DATABASE_URL` | Backend | SQLAlchemy URL, e.g. `postgresql+psycopg://USER:ENCODED_PASSWORD@HOST:5432/stockpilot` |
| `TEST_DATABASE_URL` | Tests only | Optional PostgreSQL database **ending in `_test`**; otherwise isolated temporary SQLite |
| `BASE_URL` | Smoke, load and browser tests | Defaults to `http://localhost:3000` |
| `AWS_DEPLOY_ENABLED` | GitHub repository variable | Keep unset/false until costs and cluster access are authorized |
| `AWS_ROLE_ARN`, `EKS_CLUSTER_NAME`, `INGRESS_HOST` | GitHub variables | Required only for enabled EKS deployment |
| `GHCR_PULL_SECRET` | GitHub variable | Optional existing durable registry Secret name when packages are private |
| `DEPLOY_RUNNER` | GitHub variable | Optional runner label with access to the EKS endpoint allowlist |

Alembic creates `products` and `stock_movements`. Compose runs a one-shot migration service before the API. Helm runs one ordinary migration Job per release revision; backend readiness checks both connectivity and the migrated table. Replicas do not run migrations independently. Review backwards compatibility before a migration; Helm rollback does not reverse database changes.

## Develop and test

Python 3.12+, Node 24, and an existing local PostgreSQL database are needed for normal development.

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install --require-hashes -r backend/requirements-dev.txt
export DATABASE_URL='postgresql+psycopg://stockpilot:YOUR_URL_SAFE_PASSWORD@localhost:5432/stockpilot'
cd backend
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```bash
cd frontend
npm ci --ignore-scripts
npm run dev
```

Tests never use `DATABASE_URL` for test data. PostgreSQL test setup rejects names without the `_test` suffix. The convenient local suite uses temporary SQLite files; CI additionally runs the real PostgreSQL concurrency test.

```bash
cd backend
../.venv/bin/pytest -v --cov=app --cov-report=term-missing
../.venv/bin/ruff check .
../.venv/bin/ruff format --check .
cd ../frontend
npm run lint && npm test && npm run build
cd ../e2e
npm ci
npx playwright install --with-deps chromium
npm test
```

See [TESTING.md](docs/TESTING.md) for results and migration/concurrency checks.

## API

| Method | Endpoint | Behavior |
|---|---|---|
| GET | `/`, `/health`, `/ready`, `/metrics` | Service metadata, independent liveness, database/schema readiness, Prometheus metrics |
| GET | `/api/products` | Search name/SKU; filter category or `all/healthy/low/out`; `offset`/`limit` pagination |
| GET | `/api/products/{id}` | Product or 404 |
| POST | `/api/products` | Create product and opening movement in one transaction; 201 |
| PUT | `/api/products/{id}` | Replace product details; change quantity through adjustments instead |
| DELETE | `/api/products/{id}` | Delete catalog record; retain ledger snapshots; 204 |
| GET | `/api/inventory/stats` | Counts, value, categories and seven-day unit flow |
| GET | `/api/inventory/movements` | Latest-first ledger, optional `product_id`, pagination |
| POST | `/api/inventory/adjustments` | Signed non-zero quantity and reason; atomic update plus movement; 201 |

Validation errors return 422, missing products 404, duplicate SKUs/insufficient stock 409, and database failures a sanitized 503. Maximum stock is 1,000,000 units per product. One Uvicorn worker per container keeps per-process Prometheus metrics unambiguous; scale with replicas.

## Delivery, infrastructure and monitoring

[DEPLOYMENT.md](docs/DEPLOYMENT.md) contains the exact commands. The pipeline runs PostgreSQL migrations and tests, frontend quality/build, Compose smoke and browser tests, Terraform/Helm checks, separate frontend/backend builds, and blocking Trivy scans for OS and application HIGH/CRITICAL vulnerabilities. Only the scanned image archives are published. Both use the exact source SHA, never `latest`:

```text
ghcr.io/not-so-shubh/stockpilot-backend:<40-character-commit-sha>
ghcr.io/not-so-shubh/stockpilot-frontend:<40-character-commit-sha>
```

The disposable kind job validates Helm, two replicas, ClusterIP Services, actual Traefik routing, metrics-server/HPA, a live Prometheus target, and a provisioned Grafana dashboard. The separate AWS deploy job is skipped until configured; it uses GitHub OIDC and namespace-scoped EKS edit access. GHCR packages initially may be private: make them public or provision a durable `read:packages` pull Secret before EKS deployment. An Actions token that expires after a job is not a durable cluster pull credential.

Terraform defines two public and two private subnets in `ap-south-1`, one NAT gateway, an EKS cluster with a restricted public API and private API, two AL2023 managed workers, EKS access entries, network addons, EBS CSI with Pod Identity, and optional GitHub deployment role. EKS creates its cluster security group; managed workers attach it for control-plane/node communication. A single NAT and single PostgreSQL replica are capstone cost/simplicity decisions, not HA production claims.

**No paid AWS resources are created by CI or by the default setup.** Before `terraform apply`, obtain an account-specific regional cost estimate and explicit authorization for the intended runtime. Capture VPC/EKS evidence, finish the demo, then uninstall LoadBalancers and PVCs before an authorized `terraform destroy`.

## Security and operational scope

This is a single-workspace capstone, without user authentication or RBAC in the application. Use synthetic inventory for a public demonstration; add authentication, TLS, authorization, backups and restore testing before business use. API validation, safe ORM parameters, non-negative stock constraints, non-root/read-only containers, dropped capabilities, external Kubernetes Secrets, restricted EKS access, scan gates, and dependency locks provide useful controls without claiming complete security.

Do not commit `.env`, AWS keys, kubeconfigs, registry tokens or Terraform state. Kubernetes Secrets are base64-encoded, not encrypted by that encoding; apply account encryption/access controls. Trivy has no ignored CVEs or `continue-on-error` gate. See [the real scan status](docs/EVIDENCE.md); a scanner failure blocks publication until remediated.

For deployment problems, start with [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md). For instructor questions and the final live commit→pipeline→deployment sequence, use [DEMO.md](docs/DEMO.md). Submit the repository URL, evidence index, complete rubric audit, and your own demonstration/recording. AWS provisioning, destroy, and presentation marks require actual evidence, not configuration files alone.

## Lessons learned

- Real mobile actions exposed an escaped accessible table label that screenshots alone missed; containing it restored the viewport and reliable taps.
- A current Debian base still carried HIGH CVEs. The security gate blocked publication, and a maintained Alpine runtime passed the same gate after PostgreSQL/browser revalidation.
- Traefik 42 moved Service type under `service.spec.type`; checking the rendered resource caught the ignored legacy setting.
- CI evidence needs source revisions and artifact provenance. Historical screenshots must never be uploaded as proof of a new failed run.

GitOps uses optional Flux pull reconciliation with reviewed SHA promotion. See [GitOps](gitops/README.md), [security gates](security/README.md), and [the complete homework alignment](docs/HOMEWORK-ADDENDUM.md).

## Attribution

StockPilot's application/domain/schema/design are original. The reference DevOps architecture and rubric came from [Nency-Ravaliya/devops-heros](https://github.com/Nency-Ravaliya/devops-heros/tree/main/session21-python), MIT licensed. See [NOTICE.md](NOTICE.md), `LICENSE`, and `LICENSE.reference`.

Before submitting, complete [the final execution and capture checklist](docs/SUBMISSION.md).

## Final presentation pack

[Trivy explanation](docs/TRIVY-EXPLANATION.md) · [12-minute and short demo scripts](docs/FINAL-DEMO-SCRIPT.md) · [Capture checklist](docs/FINAL-PRESENTATION-CHECKLIST.md) · [Instructor Q&A](docs/INSTRUCTOR-QA.md) · [AWS readiness and cost estimate](docs/AWS-READINESS.md)

The audit distinguishes VERIFIED (83 points), READY FOR DEMO (4), BLOCKED on AWS (11), and EXCLUDED form submission (2). These are evidence categories, not awarded marks. The latest reviewed full run is pinned above; each later main run archives its own `evidence/<source-sha>` manifest.
