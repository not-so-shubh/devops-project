# Verified evidence and submission record

## Real EKS runtime update — 18 October 2026

The user subsequently completed the approved worker repair and deployed source `84c18de84538a74a8bab92b89dc72d6e89a393d0` to real EKS in Sydney. Its [CI run 39101728492](https://github.com/not-so-shubh/devops-project/actions/runs/39101728492) succeeded; AWS CI deployment remained skipped. Two workers are Ready, the Helm release is deployed, both application Deployments have two ready replicas, the database has a Bound 5 GiB gp3 PVC, and the HTTP ingress CRUD smoke passed. Actual Prometheus verification found two UP application targets and positive request traffic; HPA CPU metrics work. Authenticated Grafana API access, its four configured panels, datasource health and a live application query also passed.

See [actual runtime results and provenance](AWS-EKS-RUNTIME-VERIFICATION.md), [aggregate JSON](evidence/aws-eks-runtime-summary.json), and [private browser-capture procedure](AWS-EKS-CAPTURE.md). The public aggregates omit account-specific infrastructure identifiers. Raw CloudShell evidence remains private.

AWS organization policy explicitly denied listing OIDC providers, and a targeted GitHub-provider lookup also returned AccessDenied. The AWS deployment job remains disabled; manual Helm installation must not be described as automated EKS deployment. Browser captures, a completed student presentation and actual teardown are not yet verified. Final cleanup requires separate approval.

## Later verification and AWS CloudShell progress

The subsequent frontend lockfile-audit source `952128e01e9afed9a0349faf7c7b58d04e5a96b5` completed [run 39071726194](https://github.com/not-so-shubh/devops-project/actions/runs/39071726194) successfully, including all enabled quality, infrastructure, Compose, image-security, publishing and Kubernetes jobs. Its [immutable final verification](https://github.com/not-so-shubh/devops-project/blob/15806a25b911c264721f2dbe0316627d102da2ac/docs/FINAL-VERIFICATION.md) preserves the source-specific audit. AWS deployment was skipped; this CI result is not AWS provisioning evidence. Later workflow changes require their own validation.

On **18 October 2026 IST**, the user executed Terraform in AWS CloudShell in **Sydney (`ap-southeast-2`)** and supplied screenshots plus complete terminal output. The checkout was confirmed as `952128e01e9a`. Terraform 1.14.7 initialized locked, signed AWS provider 6.69.1 and validated successfully. The actual command `terraform -chdir=terraform plan -input=false -no-color -out=aws-review.tfplan` produced **33 to add, 0 to change, 0 to destroy**. The [sanitized plan](https://github.com/not-so-shubh/devops-project/blob/0d6856f41879c2d08ddec329b3765393cbecf7e6/docs/evidence/aws-sydney-plan.txt), [provenance/preflight JSON](https://github.com/not-so-shubh/devops-project/blob/0d6856f41879c2d08ddec329b3765393cbecf7e6/docs/evidence/aws-sydney-review.json), and [regional cost review](https://github.com/not-so-shubh/devops-project/blob/0d6856f41879c2d08ddec329b3765393cbecf7e6/docs/AWS-SYDNEY-PLAN-REVIEW.md) are durable evidence for M7.3. This is user-provided actual CloudShell execution reviewed by the assistant, not independently executed AWS commands from this workspace.

The user approved the reviewed Sydney provisioning and app bootstrap at **11:04 IST**, with a proposed **$10 USD / six-hour** spending target and separate cleanup approval. A first block stopped before apply because CloudShell's egress IP had changed. The revised block refreshed only the private `/32` allowlist, regenerated the 33-create plan, verified the scope again, and reached its apply start marker at **05:42:07 UTC / 11:12:07 IST**. At that initial checkpoint the supplied transcript ended at the start marker. Later provisioning and runtime results supersede that checkpoint, as recorded in the update above; cleanup remains unverified. Private state, real tfvars, saved binary plans and credentials are excluded from public Git. The spending target has no automatic cutoff, and costs continue until resources are deleted.

## Earlier reviewed baseline

An earlier reviewed complete run is [StockPilot CI/CD #18](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297), **success**, executed on 17 October 2026. Its source is `710d1460abc480d8b19e2b98f648a9a5c1c23339`. Evidence is pinned to commit `a4b8d43d2125d25fc54cc702f68e8361c684fc8b` so links identify the checked snapshot. Newer source changes need their own successful run; the files below remain proof of this specified revision.

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

Use [SUBMISSION.md](SUBMISSION.md) for the exact remaining actions and screenshot-format checklist, [all 46 criteria](RUBRIC-CHECKLIST.md) for the evidence-based audit, and [DEMO.md](DEMO.md) for the walkthrough. The earlier baseline audit supported 39 criteria covering 83 rubric points; that historical count predates the real AWS progress above and is neither an awarded nor guaranteed grade. AWS plan and provisioning have subsequent executed evidence. Cleanup, the AWS OIDC deployment blocker, remaining browser captures and student performance must be tracked separately; a final audit follows evidence completion. Official form submission is **Student action — excluded from this task**.

## Earlier workspace checks and prepared materials

[Local Terraform readiness output](evidence/terraform-local-readiness.txt) preserves command results and environment limitations. [Cloud access check](evidence/cloud-access-check.json) records that no AWS identity, permission verification, plan, apply or destroy had occurred from this workspace at that earlier checkpoint. It predates the user's subsequent CloudShell execution. [Local regression output](evidence/regression-local.txt) distinguishes SQLite checks from CI PostgreSQL/container checks. [AWS readiness](AWS-READINESS.md) records architecture review, public regional pricing and the secure connection/approval requirements. These files are not AWS execution proof.

The UI quick guide now explains the already enforced overselling rule. The source-pinned run above completed a real pipeline and disposable deployment with that UI change plus the libexpat security fix; its `ci-run.json` identifies the exact source and artifact origins. This technical chain does not represent a student presentation or an EKS deployment.

The first presentation-pack rebuild [39070263226](https://github.com/not-so-shubh/devops-project/actions/runs/39070263226) failed the frontend security gate on libexpat CVE-2026-77214. It did not publish the images or deploy Kubernetes. The failure is preserved in [trivy-frontend-blocked-summary.json](evidence/trivy-frontend-blocked-summary.json), with a full report on its evidence branch. The subsequent source `710d146` requires the fixed Alpine package and passed the complete source-pinned run above. The failed run remains archived independently; its blocked frontend was not promoted.

Final report review found the static image's Node inventory contained only the root frontend package. An additional blocking npm audit now checks the full frontend lockfile graph, including dev/build dependencies, and archives `frontend-sca.json`. The older pinned run above predates that gate; verify the added check using its final source's own `ci-run.json` and report. The image scans remain blocking and unchanged.
