# Verified evidence and submission record

The latest reviewed complete run is [StockPilot CI/CD #18](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297), **success**, executed on 17 October 2026. Its source is `710d1460abc480d8b19e2b98f648a9a5c1c23339`. Evidence is pinned to commit `a4b8d43d2125d25fc54cc702f68e8361c684fc8b` so links identify the checked snapshot. Newer source changes need their own successful run; the files below remain proof of this specified revision.

| Area | Actual verified result | Original evidence |
|---|---|---|
| Backend | 44 PostgreSQL tests passed, including concurrency; 97.67% coverage | [pytest-postgres.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/pytest-postgres.txt) |
| Frontend | Lint, four utility tests, production build, four desktop/mobile scenarios in Compose and again through Ingress | [quality job](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297/job/117507399251), [Compose job](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297/job/117507624611) |
| Compose | Healthy frontend/backend/PostgreSQL; completed migrations, HTTP smoke and persistence after actual database restart | [compose-ci.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/compose-ci.txt), [compose-smoke.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/compose-smoke.txt), [persistence-ci.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/persistence-ci.txt) |
| SAST and secrets | Bandit and Trivy secret gates passed | [bandit.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/bandit.json), [secrets.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/secrets.json) |
| SCA and image security | Both OS/library scans passed unchanged HIGH/CRITICAL gate | [trivy-backend.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/trivy-backend.json), [trivy-frontend.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/trivy-frontend.json) |
| GHCR | Both exact-SHA images published; anonymous manifest/layer access and source revision verified | [ghcr-backend.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/ghcr-backend.json), [ghcr-frontend.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/ghcr-frontend.json) |
| Terraform | Locked initialization, validation, formatting and mock topology test passed; no AWS plan/apply/destroy performed | [infrastructure job](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297/job/117507399134), [terraform-ci-mock-test.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/terraform-ci-mock-test.txt) |
| Kubernetes and Helm | Helm deployed; two backend and two frontend replicas, PostgreSQL/PVC, Services and actual Ingress CRUD/browser checks passed | [kubernetes-ci.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/kubernetes-ci.txt), [helm-release-ci.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/helm-release-ci.txt) |
| HPA | Resource metrics available and ScalingActive=True; no unobserved scale-out claimed | [hpa-metrics-ci.txt](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/hpa-metrics-ci.txt) |
| Monitoring | Two targets UP; positive request rate; actual authenticated Grafana screenshot has populated charts | [prometheus-targets.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/prometheus-targets.json), [prometheus-query.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/prometheus-query.json), [grafana-dashboard.png](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/grafana-dashboard.png) |
| Troubleshooting | Observed empty Service and ErrImagePull; corrected selector restored two endpoints; corrected image responded UP | [troubleshooting-ci.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/troubleshooting-ci.json) |
| GitOps | Flux fetched exact tested Git revision, upgraded Helm to revision 2, rolled APP_ENV to gitops-ci and passed final HTTP smoke | [gitops-ci.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/gitops-ci.json) |
| Provenance | All quality/build/publish/Kubernetes outcomes success, artifact origin recorded per file | [ci-run.json](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/ci-run.json) |

## Actual screenshots

These are captures of the running application and monitoring UI, not mockups. Prometheus cluster addresses are explicitly redacted in its screenshot. Grafana includes the real startup error/latency history; the graph is not edited to hide it. Compose and kind use separate synthetic databases.

### Running frontend

![Actual desktop frontend](https://raw.githubusercontent.com/not-so-shubh/devops-project/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/frontend-desktop.png)

[Mobile frontend](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/frontend-mobile.png) · [Desktop product dialog](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/create-dialog-desktop.png) · [Mobile product dialog](https://github.com/not-so-shubh/devops-project/blob/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/create-dialog-mobile.png)

### Prometheus target health

![Actual Prometheus target health: two targets UP](https://raw.githubusercontent.com/not-so-shubh/devops-project/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/prometheus-targets.png)

### Grafana live dashboard

![Actual authenticated Grafana dashboard with populated charts](https://raw.githubusercontent.com/not-so-shubh/devops-project/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence/grafana-dashboard.png)

## GitHub page and transcript captures (earlier reviewed revision)

[Green Actions summary](evidence/github-green-run.jpg) · [Backend GHCR SHA page](evidence/github-ghcr-backend.jpg) · [Frontend GHCR SHA page](evidence/github-ghcr-frontend.jpg) · [44-pass PostgreSQL transcript](evidence/github-pytest-transcript.jpg) · [Running Pods/Services/Ingress transcript](evidence/github-kubernetes-transcript.jpg) · [Healthy Compose output](evidence/github-compose-health-output.jpg)

These additional JPG images retain their original prior-revision provenance (`9462f34dc3c8f6321af23a85d11296d980839595`); they are not new captures of the current reviewed revision. The PNGs and reports above are pinned to the reviewed `710d146` evidence commit. These additional images are unmodified browser captures. The transcript images show archived actual command output on GitHub, rather than a newly executed terminal. [Capture provenance](evidence/github-screen-captures.json) records every exact page URL and the verified source. Job logs in this public browser require sign-in; original authenticated reports are already preserved above. If the instructor requires literal terminal screenshots, capture those during the live demo as listed in SUBMISSION.md.

## Durable evidence and history

The workflow archives an explicit allowlist to `evidence/<source-sha>`. `ci-run.json` records source, run, selected artifact origins and job outcomes. Each generating job clears its historical generated files before running. Failed runs stay visibly failed and do not count as green evidence. Raw browser traces and matched secret values are excluded from Git; text/JSON identifiers are redacted without changing results, severities or numeric metrics.

Earlier failed runs and the original blocked Debian image scan remain documented in [troubleshooting](TROUBLESHOOTING.md) and [security](../security/README.md). They explain the fixes, while the complete success above verifies the resulting system. Actions artifacts retain reports for 30 days and image tarballs for one day; the pinned evidence commit preserves the allowlisted outputs beyond artifact expiry.

## Final submission

Use [SUBMISSION.md](SUBMISSION.md) for the exact remaining actions and screenshot-format checklist, [all 46 criteria](RUBRIC-CHECKLIST.md) for the evidence-based audit, and [DEMO.md](DEMO.md) for the walkthrough. The checked evidence supports 39 criteria covering 83 rubric points; this is neither an awarded nor guaranteed grade. AWS plan/provision/destroy remain BLOCKED; the student security explanation and presentation are READY FOR DEMO, not verified personal performance. Official form submission is **Student action — excluded from this task**.

## Current-session checks and prepared materials

[Local Terraform readiness output](evidence/terraform-local-readiness.txt) preserves command results and environment limitations. [Cloud access check](evidence/cloud-access-check.json) records that no AWS identity, permission verification, plan, apply or destroy occurred. [Local regression output](evidence/regression-local.txt) distinguishes SQLite checks from CI PostgreSQL/container checks. [AWS readiness](AWS-READINESS.md) records architecture review, public regional pricing and the secure connection/approval requirements. These files are not AWS execution proof.

The UI quick guide now explains the already enforced overselling rule. The source-pinned run above completed a real pipeline and disposable deployment with that UI change plus the libexpat security fix; its `ci-run.json` identifies the exact source and artifact origins. This technical chain does not represent a student presentation or an EKS deployment.

The first presentation-pack rebuild [39070263226](https://github.com/not-so-shubh/devops-project/actions/runs/39070263226) failed the frontend security gate on libexpat CVE-2026-77214. It did not publish the images or deploy Kubernetes. The failure is preserved in [trivy-frontend-blocked-summary.json](evidence/trivy-frontend-blocked-summary.json), with a full report on its evidence branch. The subsequent source `710d146` requires the fixed Alpine package and passed the complete source-pinned run above. The failed run remains archived independently; its blocked frontend was not promoted.

Final report review found the static image's Node inventory contained only the root frontend package. An additional blocking npm audit now checks the full frontend lockfile graph, including dev/build dependencies, and archives `frontend-sca.json`. The older pinned run above predates that gate; verify the added check using its final source's own `ci-run.json` and report. The image scans remain blocking and unchanged.
