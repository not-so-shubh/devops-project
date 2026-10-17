# Attached homework alignment

The supplied “Session 21: Final DevOps Project & Troubleshooting” PDF supplements the authoritative 100-point GRADING.md. It adds SAST, SCA, secret scanning, ConfigMap, GitOps, logs and lessons learned.

| PDF deliverable | Implementation / verification |
|---|---|
| application/ | `backend/` and `frontend/` (original StockPilot; root organization follows the user's explicit requirement) |
| docker/ | Component Dockerfiles and root Compose, documented in README |
| kubernetes/ | `k8s/` namespace and `helm/stockpilot/templates/` |
| ConfigMap | `helm/stockpilot/templates/configmap.yaml`, non-secret runtime environment |
| SAST / SCA / secrets / images / gates | `security/README.md`, Bandit and Trivy CI reports; actual run status remains authoritative |
| GitOps | `gitops/`, reviewed immutable-SHA Flux HelmRelease promotion plus disposable Flux reconciliation gate; check actual `gitops-ci.json` result |
| logs / metrics | Structured Uvicorn access logs, `/metrics`, Prometheus/Grafana, CI diagnostics |
| Multiple intentional issues | Isolated bad-image and incorrect-Service-selector exercises in TROUBLESHOOTING; automated diagnose/repair/verify lab; actual observations in `troubleshooting-ci.json` after success |
| Screenshots and lessons | EVIDENCE, TROUBLESHOOTING and lessons below |

## Lessons learned from actual implementation

* PostgreSQL-backed tests catch concurrency behavior that SQLite cannot establish. The CI suite exercises simultaneous stock reductions.
* A mobile screenshot alone was insufficient: desktop passed while mobile clicks hit the wrong coordinates. An absolutely positioned screen-reader label escaped its table scroll container. Giving that container `position: relative` restored the 390px mobile viewport; all four Compose desktop/mobile tests then passed. Browser tests now compare document width to the visual viewport and perform real inventory operations.
* Migration hooks can deadlock initial installs when PostgreSQL has not started. An ordinary revisioned migration Job and readiness checks permit database startup and migrations before application readiness.
* Evidence must distinguish configuration validation, disposable-cluster runtime proof and paid AWS provisioning. A Terraform mock plan cannot prove that an AWS account was provisioned or cleaned up.
* GitOps and direct Helm CI must have one designated release owner; enabling both creates competing desired states.
