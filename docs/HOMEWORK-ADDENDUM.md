# Attached homework alignment

[Documentation hub](README.md) · [Current evidence index](EVIDENCE.md)

The historical supplementary receipts below retain their original source labels. The current verified application baseline is [8944da7 / run 39696800574](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574); its [manifest](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ci-run.json) includes the same automated gate categories.

The supplied “Session 21: Final DevOps Project & Troubleshooting” PDF supplements the authoritative 100-point GRADING.md. It adds SAST, SCA, secret scanning, ConfigMap, GitOps, logs and lessons learned.

| PDF deliverable | Implementation / verification |
|---|---|
| application/ | `application/README.md` maps to canonical `backend/` and `frontend/` (original StockPilot) |
| docker/ | `docker/README.md` maps to component Dockerfiles and root Compose |
| kubernetes/ | `kubernetes/README.md` maps to `k8s/` namespace and `helm/stockpilot/templates/` |
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

## Verified supplementary homework results

The [complete successful run](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598) passed SAST, secret/SCA/image gates, live ConfigMap/Secret/probe/storage deployment, monitoring, both troubleshooting repairs and actual Flux reconciliation. See [the original Flux record](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/gitops-ci.json), [repair observations](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/troubleshooting-ci.json) and [actual screenshot gallery](EVIDENCE.md). AWS and final submission/presentation requirements are tracked separately in [SUBMISSION.md](SUBMISSION.md).
