# Deployment runbook

[Documentation hub](README.md) · [Architecture](ARCHITECTURE.md) · [Troubleshooting](TROUBLESHOOTING.md)

## Choose the environment

| Environment | Use | Current status |
|---|---|---|
| Docker Compose | Local application/persistence walkthrough | Run locally with Docker |
| Local kind | Kubernetes/Helm/monitoring walkthrough | Optional local helper creates a new named cluster |
| GitHub Actions kind | Source-pinned automated integration | Disposable, created and removed by each run |
| Historical Sydney EKS | Real AWS provisioning/manual deployment evidence | Captured 18 October; approved cleanup verified 22 October |
| Optional Actions EKS deployment | Updating an already bootstrapped AWS release | Disabled by OIDC account-policy restrictions |

This guide does not authorize new AWS resources. The old EKS endpoint is deleted. [Historical runtime](AWS-EKS-RUNTIME-VERIFICATION.md) · [Cleanup result](AWS-CLEANUP-VERIFICATION.md).

## Local Compose

Follow the root [secure quick start](../README.md#quick-start) to create a private `.env` only if one does not exist. The password must be URL-safe because Compose places it in the database URL. Preserve the credential matching an existing initialized volume.

From the repository root:

```bash
docker compose config --quiet
docker compose up --build -d --wait --wait-timeout 180
docker compose exec backend python -m app.seed
docker compose ps
python3 scripts/smoke.py
```

Open [the app](http://localhost:3000) and [Swagger](http://localhost:8000/docs). The optional seed is explicit/idempotent. Smoke creates a uniquely named verification product and removes that catalog record while retaining its movement history.

| Setting | Meaning |
|---|---|
| `.env`: `POSTGRES_DB`, `POSTGRES_USER` | Default local names are `stockpilot` |
| `.env`: `POSTGRES_PASSWORD` | Private random URL-safe credential |
| Backend `DATABASE_URL` | SQLAlchemy URL with `postgresql+psycopg` driver |
| Test `TEST_DATABASE_URL` | Separate `_test` PostgreSQL database, otherwise temporary SQLite |
| Check/browser `BASE_URL` | Target application origin; defaults to localhost:3000 |

Compose runs PostgreSQL, a one-shot Alembic migration, the API and Nginx frontend. Application ports are loopback-only; the database is private to the network. Backend/frontend run as non-root with read-only root filesystems and temporary writable mounts.

```bash
docker compose logs -f backend
docker compose stop
docker compose up -d --wait
docker compose down
```

Stopping or running `down` retains the named database volume. `docker compose down -v` permanently removes local demo data and is a separate intentional choice after saving anything needed. [Container guide](../docker/README.md).

## Local kind

Requirements: Docker, kind, Helm, kubectl, Git and Python; the local helper recommends at least 8 GB of Docker memory. Stop Compose before reusing its local port 3000.

```bash
bash scripts/local-kind.sh
```

The helper refuses to overwrite an existing `stockpilot` kind cluster. It builds source images, loads them into digest-pinned Kubernetes 1.35.8, installs Traefik/metrics-server/monitoring, deploys the Helm chart and prints port-forwards. The generated secrets are for this disposable cluster only. This source-build helper does not replace the CI image-scan/publication gates.

In separate terminals:

```bash
kubectl port-forward -n ingress-system svc/traefik 3000:80
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
kubectl port-forward -n monitoring svc/monitoring-grafana 3001:80
```

Use localhost:3000 for the app, localhost:9090/targets for Prometheus and localhost:3001 for Grafana. Retrieve local Grafana credentials privately; keep them outside recordings. To remove only this disposable local environment after saving evidence: `kind delete cluster --name stockpilot`.

## CI images and Helm verification

Use a source SHA whose own build/scan/publish jobs succeeded. `git rev-parse HEAD` is not proof that images for that commit exist. The verified application baseline is `8944da7ddf2be0845a593c2f65482eb922e6d9f7`:

```bash
SHA=8944da7ddf2be0845a593c2f65482eb922e6d9f7
docker pull "ghcr.io/not-so-shubh/stockpilot-backend:$SHA"
docker pull "ghcr.io/not-so-shubh/stockpilot-frontend:$SHA"
helm lint helm/stockpilot --set backend.tag="$SHA" --set frontend.tag="$SHA"
```

[Anonymous-pull receipts](EVIDENCE.md#source-pinned-ci-evidence) confirm both baseline images are public. A future private package would require a durable least-privilege pull Secret; a job-scoped `GITHUB_TOKEN` is not a long-lived cluster credential.

For an already bootstrapped disposable kind environment, chart operations use `standard` storage and the localhost ingress host. The complete installation sequence is in [`scripts/local-kind.sh`](../scripts/local-kind.sh). On any existing release, preserve database/Grafana credentials. Never rerun a disposable secret generator against an existing business database.

```bash
kubectl get pods,svc,ingress,hpa -n stockpilot
kubectl rollout status deployment/stockpilot-backend -n stockpilot --timeout=180s
kubectl rollout status deployment/stockpilot-frontend -n stockpilot --timeout=180s
helm list -n stockpilot
kubectl top pods -n stockpilot
```

The migration Job is named by release revision and backend readiness waits for its schema. One release per namespace and one Helm upgrade at a time are supported. A Helm rollback restores images/values, not database state.

## Historical AWS EKS procedure

The approved Sydney execution used VPC public/private routing, EKS 1.35, two `m7i-flex.large` managed workers, EBS CSI/Pod Identity, encrypted gp3 storage, external Secrets, Traefik, resource metrics and monitoring. It deployed application source `84c18de84538a74a8bab92b89dc72d6e89a393d0` manually with Helm.

Terraform templates still default to Mumbai (`ap-south-1`) and `t3.large`; those defaults are not the executed Sydney settings or a statement about account eligibility. A future permitted deployment must choose explicit account/region/CIDRs/types, check availability/quotas/current costs, review a real plan and obtain new cost/runtime authorization. [Terraform guide](../terraform/README.md) · [AWS readiness](AWS-READINESS.md).

The detailed original operator procedures remain in [the immutable pre-polish runbook](https://github.com/not-so-shubh/devops-project/blob/8944da7ddf2be0845a593c2f65482eb922e6d9f7/docs/DEPLOYMENT.md). Treat its provisioning/bootstrap commands as historical/future-authorized procedures, not instructions to recreate the deleted demo now. Kind-only insecure kubelet TLS settings must not be copied to EKS. The historical ingress was HTTP; TLS would require an actual certificate and chart configuration.

## Optional AWS deployment

The Actions AWS job remains disabled. Provider listing was explicitly denied by organization policy, and a targeted lookup also returned AccessDenied; provider existence is unconfirmed. Do not replace this blocker with permanent AWS keys or broaden trust/network access.

A permitted future setup needs an administrator-approved OIDC provider/trust, actual repository subject claims, a protected production environment, namespace-scoped EKS access, a runner network route to the restricted API, pre-existing storage/controllers/Secrets, and verified image pulls. Only then can `AWS_DEPLOY_ENABLED` be enabled under separately authorized scope. Relevant variables and conditions are defined in [the unchanged workflow](../.github/workflows/ci-cd.yml) and [Terraform](../terraform/README.md). Flux and direct Actions must not both continuously own one release.

## Monitoring and cleanup

[Monitoring](../monitoring/README.md) documents real metric names, port-forwards, target selection and HPA inputs. A CPU metric at low load does not prove autoscaling occurred.

The real final cleanup was separately approved. The operator removed LB/PVC assets and waited for AWS deletion while controllers remained alive, removed monitoring, then applied the saved 33-resource destroy plan. Empty state and scoped residual checks passed. [Exact result, command boundary and backup](AWS-CLEANUP-VERIFICATION.md).

Do not rerun that completed plan. The private state, saved plans, dump and command logs stay outside Git; actual billing totals/credits remain unverified.
