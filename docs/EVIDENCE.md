# Evidence index

[Documentation hub](README.md) · [Examiner handoff](FINAL-PROJECT-HANDOFF.md) · [Rubric audit](RUBRIC-CHECKLIST.md)

This index distinguishes source-pinned CI/kind proof from user-executed historical AWS evidence. A successful pipeline does not establish automatic EKS deployment or a student's personal presentation.

## Source-pinned CI evidence

The verified application/security baseline is **`8944da7ddf2be0845a593c2f65482eb922e6d9f7`**, [run 39696800574](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574), completed successfully on 22 October. Its immutable evidence commit is **`fa40366375c8a05edbe6a0837071e988d496e62b`**. [Manifest, source and job results](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ci-run.json).

| Claim | Original receipt |
|---|---|
| 44 PostgreSQL passes, 97.67% coverage | [pytest-postgres.txt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/pytest-postgres.txt) |
| Compose health/non-root/HTTP proof | [compose-ci.txt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/compose-ci.txt) · [smoke](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/compose-smoke.txt) |
| Records survive PostgreSQL container restart | [persistence-ci.txt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/persistence-ci.txt) |
| Frontend/backend HIGH/CRITICAL findings: zero | [Backend Trivy](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/trivy-backend.json) · [Frontend Trivy](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/trivy-frontend.json) |
| Frontend audit: 124 dependencies, zero reported vulnerabilities | [frontend-sca.json](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/frontend-sca.json) |
| SAST/secret gates | [Bandit](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/bandit.json) · [sanitized secret report](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/secrets.json) |
| Public SHA images and non-root identities | [Backend GHCR](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ghcr-backend.json) · [Frontend GHCR](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ghcr-frontend.json) |
| Terraform mock/Helm checks | [Terraform validation](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/terraform-ci-validate.txt) · [mock topology](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/terraform-ci-mock-test.txt) |
| Real disposable kind readiness/Helm/ingress/HPA | [Kubernetes output](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/kubernetes-ci.txt) · [cluster health](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/cluster-health-ci.json) · [resource metrics](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/hpa-metrics-ci.txt) |
| UP targets and positive live traffic | [Targets](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/prometheus-targets.json) · [query](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/prometheus-query.json) |
| Selector and image-pull faults repaired | [Observations](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/troubleshooting-ci.json) · [investigation](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/troubleshooting-investigation-ci.txt) |
| Flux fetched the tested SHA; release revision 2 Ready | [gitops-ci.json](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/gitops-ci.json) |

Current main has a [dynamic workflow status](https://github.com/not-so-shubh/devops-project/actions/workflows/ci-cd.yml). Each later source archives its own receipts on `evidence/<source-sha>`. Inspect the matching `ci-run.json` and actual job results before calling that source verified. Image tarballs have short artifact retention; immutable allowlisted report commits retain the cited proof.

## Genuine screenshots

| Capture | Environment and provenance |
|---|---|
| [EKS desktop](evidence/eks-frontend-desktop.png) / [mobile](evidence/eks-frontend-mobile.png) | Real manual Sydney EKS deployment, 18 October; [review/hashes](AWS-EKS-CAPTURE-REVIEW.md) |
| [CI desktop](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/frontend-desktop.png) / [mobile](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/frontend-mobile.png) | Actual Compose browser capture for source `8944da7` |
| [Prometheus Targets](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/prometheus-targets.png) | Disposable kind, same source/run |
| [Grafana dashboard](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/grafana-dashboard.png) | Authenticated live kind dashboard, same source/run |

Real EKS Prometheus/Grafana originals and raw AWS JSON remain in the private supplied archives. The public [capture aggregate](evidence/aws-eks-capture-review.json) records the reviewed hashes. The refreshed EKS archive SHA-256 is `825d31a399760031c5054cb7076c8ef0748ba827492ad50311fefa9bbbd330eb`; live API and original screenshot confirmed the corrected **0–100%** error axis and sampled **2.1333333333333333 requests/second**.

## Historical AWS lifecycle

| Phase | Execution and source |
|---|---|
| Original plan, 18 October | Actual CloudShell Terraform 1.14.7 / AWS provider 6.69.1 plan: 33 additions; [sanitized plan](https://github.com/not-so-shubh/devops-project/blob/0d6856f41879c2d08ddec329b3765393cbecf7e6/docs/evidence/aws-sydney-plan.txt), [preflight/provenance](https://github.com/not-so-shubh/devops-project/blob/0d6856f41879c2d08ddec329b3765393cbecf7e6/docs/evidence/aws-sydney-review.json) |
| Apply/repair | Approved Sydney provisioning; failed empty worker group repaired under separate reviewed scope; two Ready `m7i-flex.large` workers |
| Manual app/runtime | Application source `84c18de84538a74a8bab92b89dc72d6e89a393d0`; [runtime record](AWS-EKS-RUNTIME-VERIFICATION.md) and [aggregate](evidence/aws-eks-runtime-summary.json) |
| Original capture | Tool source `cf87b82`; archive SHA-256 `8d356ef8daae273b6869b16d2f5da3a1b149ab884269eb1a64bc0263a6ce2128`; actual start 09:30:20 UTC on 18 October |
| Refreshed capture | Tool source `13d2bf1`; start 09:57:29 UTC / browser 09:59:03 UTC on 18 October; [exact record](AWS-EKS-CAPTURE-REVIEW.md#refreshed-monitoring-capture) |
| Approved cleanup | Helper source `228cccd`; user-executed result at **05:16:28 IST on 22 October**; [verification](AWS-CLEANUP-VERIFICATION.md) and [actual aggregate](evidence/aws-cleanup-summary.json) |

Terraform state is empty. The identified EKS/LB/VPC/NAT/EIP/roles/log group and three EBS disks are gone; two workers terminated and zero matching ENIs remain. The private database dump's downloaded/uploaded SHA-256 matched. Actual billing totals/credits were not checked. The original six-hour runtime window was exceeded.

The executed deletion command applied a saved `terraform plan -destroy` plan. The record does not claim the literal `terraform destroy` command was typed. AWS outputs were supplied by the user and reviewed; the assistant did not hold a direct authenticated AWS session.

## Preserved chronology and failed gates

| Checkpoint | What it establishes |
|---|---|
| [38999948371](https://github.com/not-so-shubh/devops-project/actions/runs/38999948371) | Original backend Debian findings blocked promotion; [retained summary](evidence/trivy-backend-blocked-summary.json) |
| [39000262612](https://github.com/not-so-shubh/devops-project/actions/runs/39000262612) | Alpine image scans passed; this was not the final fully green cluster run |
| [39045365598](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598) | Earlier complete runtime/monitoring/troubleshooting/Flux proof, source `9462f34` |
| [39070263226](https://github.com/not-so-shubh/devops-project/actions/runs/39070263226) | Frontend libexpat HIGH finding blocked promotion; [retained summary](evidence/trivy-frontend-blocked-summary.json) |
| [39070661297](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297) | Source `710d146`, fixed libexpat and fully green follow-up; [original archive](https://github.com/not-so-shubh/devops-project/tree/a4b8d43d2125d25fc54cc702f68e8361c684fc8b/docs/evidence) |
| [39117229787](https://github.com/not-so-shubh/devops-project/actions/runs/39117229787) | Source `13d2bf1`, earlier complete green evidence; [archive](https://github.com/not-so-shubh/devops-project/tree/64aba88dbea754bff364e12d2fc589f4b2b0df41/docs/evidence) |
| [39694461786](https://github.com/not-so-shubh/devops-project/actions/runs/39694461786) | Frontend libx11 HIGH finding blocked promotion; [retained summary](evidence/trivy-frontend-libx11-blocked-summary.json) |
| [39696800574](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574) | Source `8944da7`, libx11 1.8.14-r0, both image gates and full enabled pipeline passed |

Older workspace failures/local SQLite checks, original `.txt`/`.log` reports, screenshots and source-specific JSON remain in [`evidence/`](evidence/). They retain their original environment/date labels. [Pre-polish evidence chronology](https://github.com/not-so-shubh/devops-project/blob/8944da7ddf2be0845a593c2f65482eb922e6d9f7/docs/EVIDENCE.md) preserves the full earlier narrative. None of those files are rewritten as evidence of a fresh run.

## Presentation and remaining assessment

[Real supplied PowerPoint](presentation/README.md) and its rendered preview are available. **No actual demo video was supplied**; [recording guide](demo/README.md). Adding either guide does not complete personal assessment.

The audit covers **43 criteria / 94 technical points**, with **4 personal explanation/demo points** and **2 excluded form points**, not awarded marks. The EKS Actions job remains disabled by OIDC policy; manual EKS and automatic kind evidence remain separate. Exact Console/terminal screenshot formats depend on genuine saved captures. [Submission checklist](SUBMISSION.md).

Private state, plans, credentials, database contents and account/resource identifiers are excluded from this public evidence index. Official form: **Student action — excluded from this task**.
