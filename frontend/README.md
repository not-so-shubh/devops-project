# Frontend

[Documentation hub](../docs/README.md) · [Full-stack quick start](../README.md#quick-start) · [Browser tests](../docs/TESTING.md#frontend-and-browser-checks)

React/Vite implements the inventory workspace: searchable product catalog, accessible edit/detail dialogs, controlled stock adjustments, a retained ledger, live statistics and CSV export. Values come from the API; optional demo seed records live in PostgreSQL.

## Development

Use Node 24 to match CI; [`package.json`](package.json) declares the minimum engine requirement. Run an API on localhost:8000, then from the repository root:

```bash
npm --prefix frontend ci --ignore-scripts
npm --prefix frontend run dev
```

Vite prints its actual local URL. Its development proxy forwards `/api`, `/docs` and `/openapi.json` to localhost:8000. If Compose already occupies a port, stop that frontend or pass an available Vite `--port`; do not assume the Vite server uses Compose's port 3000.

```bash
npm --prefix frontend run lint
npm --prefix frontend test
npm --prefix frontend run build
```

The four utility tests cover stock-status boundaries, CSV/formula safety, validation error display and empty deletion responses. Playwright separately performs real desktop/mobile actions against a running application.

## Container and request routing

The [multi-stage Dockerfile](Dockerfile) builds locked Node dependencies, then serves static output through unprivileged Nginx as UID 101 on port 8080. [`nginx.conf`](nginx.conf) supports SPA navigation, `/healthz` and an unchanged `/api` proxy to backend:8000. No environment-specific cluster URL is compiled into the bundle.

Runtime dependency manifests remain outside the web root. Trivy inventories OS/supported image packages, while a separate full lockfile audit includes build/development dependencies. The historical libexpat/libx11 findings and fixes are recorded in [security](../security/README.md).

## UI evidence

[Genuine historical EKS desktop](../docs/evidence/eks-frontend-desktop.png) · [Mobile](../docs/evidence/eks-frontend-mobile.png) · [Capture provenance](../docs/AWS-EKS-CAPTURE-REVIEW.md).

The mobile acceptance checks document/client/visual viewport widths and performs CRUD, filters, export, navigation and dialogs. The supplied presentation's editable interface illustration is labelled as an illustration; it is not the screenshot evidence linked here.
