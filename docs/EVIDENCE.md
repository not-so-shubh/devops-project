# Verified evidence and submission record

The latest reviewed complete run is [StockPilot CI/CD #13](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598), **success**, executed on 17 October 2026. Its source is `9462f34dc3c8f6321af23a85d11296d980839595`. Evidence is pinned to commit `48bd7092be1c403e91fc08717f75b53c61bf4295` so links identify the checked snapshot. Newer source changes need their own successful run; the files below remain proof of this specified revision.

| Area | Actual verified result | Original evidence |
|---|---|---|
| Backend | 44 PostgreSQL tests passed, including concurrency; 97.67% coverage | [pytest-postgres.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/pytest-postgres.txt) |
| Frontend | Lint, four utility tests, production build, four desktop/mobile scenarios in Compose and again through Ingress | [quality job](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598/job/117433008105), [Compose job](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598/job/117433188546) |
| Compose | Healthy frontend/backend/PostgreSQL; completed migrations, HTTP smoke and persistence after actual database restart | [compose-ci.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/compose-ci.txt), [compose-smoke.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/compose-smoke.txt), [persistence-ci.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/persistence-ci.txt) |
| SAST and secrets | Bandit and Trivy secret gates passed | [bandit.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/bandit.json), [secrets.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/secrets.json) |
| SCA and image security | Both OS/library scans passed unchanged HIGH/CRITICAL gate | [trivy-backend.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/trivy-backend.json), [trivy-frontend.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/trivy-frontend.json) |
| GHCR | Both exact-SHA images published; anonymous manifest/layer access and source revision verified | [ghcr-backend.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/ghcr-backend.json), [ghcr-frontend.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/ghcr-frontend.json) |
| Terraform | Locked initialization, validation, formatting and mock topology test passed; no AWS plan/apply/destroy performed | [infrastructure job](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598/job/117433007924), [terraform-ci-mock-test.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/terraform-ci-mock-test.txt) |
| Kubernetes and Helm | Helm deployed; two backend and two frontend replicas, PostgreSQL/PVC, Services and actual Ingress CRUD/browser checks passed | [kubernetes-ci.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/kubernetes-ci.txt), [helm-release-ci.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/helm-release-ci.txt) |
| HPA | Resource metrics available and ScalingActive=True; no unobserved scale-out claimed | [hpa-metrics-ci.txt](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/hpa-metrics-ci.txt) |
| Monitoring | Two targets UP; positive request rate; actual authenticated Grafana screenshot has populated charts | [prometheus-targets.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/prometheus-targets.json), [prometheus-query.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/prometheus-query.json), [grafana-dashboard.png](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/grafana-dashboard.png) |
| Troubleshooting | Observed empty Service and ErrImagePull; corrected selector restored two endpoints; corrected image responded UP | [troubleshooting-ci.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/troubleshooting-ci.json) |
| GitOps | Flux fetched exact tested Git revision, upgraded Helm to revision 2, rolled APP_ENV to gitops-ci and passed final HTTP smoke | [gitops-ci.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/gitops-ci.json) |
| Provenance | All quality/build/publish/Kubernetes outcomes success, artifact origin recorded per file | [ci-run.json](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/ci-run.json) |

## Actual screenshots

These are captures of the running application and monitoring UI, not mockups. Prometheus cluster addresses are explicitly redacted in its screenshot. Grafana includes the real startup error/latency history; the graph is not edited to hide it. Compose and kind use separate synthetic databases.

### Running frontend

![Actual desktop frontend](https://raw.githubusercontent.com/not-so-shubh/devops-project/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/frontend-desktop.png)

[Mobile frontend](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/frontend-mobile.png) · [Desktop product dialog](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/create-dialog-desktop.png) · [Mobile product dialog](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/create-dialog-mobile.png)

### Prometheus target health

![Actual Prometheus target health: two targets UP](https://raw.githubusercontent.com/not-so-shubh/devops-project/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/prometheus-targets.png)

### Grafana live dashboard

![Actual authenticated Grafana dashboard with populated charts](https://raw.githubusercontent.com/not-so-shubh/devops-project/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/grafana-dashboard.png)

## GitHub page and transcript captures

[Green Actions summary](evidence/github-green-run.jpg) · [Backend GHCR SHA page](evidence/github-ghcr-backend.jpg) · [Frontend GHCR SHA page](evidence/github-ghcr-frontend.jpg) · [44-pass PostgreSQL transcript](evidence/github-pytest-transcript.jpg) · [Running Pods/Services/Ingress transcript](evidence/github-kubernetes-transcript.jpg) · [Healthy Compose output](evidence/github-compose-health-output.jpg)

These additional images are unmodified browser captures. The transcript images show archived actual command output on GitHub, rather than a newly executed terminal. [Capture provenance](evidence/github-screen-captures.json) records every exact page URL and the verified source. Job logs in this public browser require sign-in; original authenticated reports are already preserved above. If the instructor requires literal terminal screenshots, capture those during the live demo as listed in SUBMISSION.md.

## Durable evidence and history

The workflow archives an explicit allowlist to `evidence/<source-sha>`. `ci-run.json` records source, run, selected artifact origins and job outcomes. Each generating job clears its historical generated files before running. Failed runs stay visibly failed and do not count as green evidence. Raw browser traces and matched secret values are excluded from Git; text/JSON identifiers are redacted without changing results, severities or numeric metrics.

Earlier failed runs and the original blocked Debian image scan remain documented in [troubleshooting](TROUBLESHOOTING.md) and [security](../security/README.md). They explain the fixes, while the complete success above verifies the resulting system. Actions artifacts retain reports for 30 days and image tarballs for one day; the pinned evidence commit preserves the allowlisted outputs beyond artifact expiry.

## Final submission

Use [SUBMISSION.md](SUBMISSION.md) for the exact remaining actions and screenshot-format checklist, [all 46 criteria](RUBRIC-CHECKLIST.md) for the evidence-based audit, and [DEMO.md](DEMO.md) for the walkthrough. The checked evidence supports 39 criteria covering 83 rubric points; this is neither an awarded nor guaranteed grade. AWS plan/provision/destroy and student submission/presentation remain unverified.
