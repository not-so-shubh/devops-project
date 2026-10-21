# Submission status and remaining work

Repository: https://github.com/not-so-shubh/devops-project

The pinned completed CI baseline is `13d2bf1481ef498670637914441452367d996aa3`: [run 39117229787](https://github.com/not-so-shubh/devops-project/actions/runs/39117229787), with [durable CI evidence](https://github.com/not-so-shubh/devops-project/tree/64aba88dbea754bff364e12d2fc589f4b2b0df41/docs/evidence). Check the [current source's Actions result](https://github.com/not-so-shubh/devops-project/actions/workflows/ci-cd.yml) and its own evidence branch for later changes. Real EKS application source is `84c18de84538a74a8bab92b89dc72d6e89a393d0`. [The inspected EKS archive review](AWS-EKS-CAPTURE-REVIEW.md) records exact provenance and original-file hashes.

## Evidence-backed status

All 46 official criteria are listed in [RUBRIC-CHECKLIST.md](RUBRIC-CHECKLIST.md). There are **43 VERIFIED criteria / 94 technical points**, **4 READY FOR DEMO points**, and **2 EXCLUDED form points**. This is evidence coverage, not an awarded grade.

Real provider-backed Terraform plan, VPC with two public/two private subnets across two AZs, active routing, EKS and managed workers are executed and independently reviewed. At capture, two workers were Ready. Real EKS Helm/PVC/replicas/ingress/HPA, four desktop/mobile browser scenarios, Prometheus UP targets and authenticated populated Grafana have actual proof. The environment was subsequently deleted after explicit approval; [cleanup and residual checks passed](AWS-CLEANUP-VERIFICATION.md).

| Remaining criterion | Points | Required completion |
|---|---:|---|
| M3.1 | 2 | **Student action — excluded from this task.** No official form opened, populated or submitted. |
| M6.3 | 1 | Personally explain the real Trivy result and limits using [TRIVY-EXPLANATION.md](TRIVY-EXPLANATION.md). Written preparation is complete; personal understanding has not been assessed. |
| M10.2 | 3 | Personally present live or produce an accepted remote recording of a genuine commit → green CI → observed deployment update. Automatic kind/Flux and manual real EKS proof are distinct. |

The mission's additional automatic AWS deployment requirement is **BLOCKED**: organization policy explicitly denied OIDC-provider listing and the exact-provider lookup also returned AccessDenied. GitHub administrator access and login succeeded. The AWS deploy job remains disabled/skipped. A permitted account-policy configuration is required; manual EKS deployment does not close that gap.

## Required screenshot and recording formats

| Requested item | Current proof / next action |
|---|---|
| Running app, desktop/mobile | Original real EKS screenshots inspected and linked in [capture review](AWS-EKS-CAPTURE-REVIEW.md). |
| Terraform non-empty plan | Actual 33-create plan and private original transcript available; retain/capture the literal terminal image. |
| AWS Console VPC / EKS | Real CLI/API resources verified. Supply pre-deletion Console screenshots already saved. The environment is deleted; CLI JSON cannot recreate genuine Console screenshots. Keep identifiers private. |
| Ready workers / Pods / Services / Helm list | Genuine private EKS output archive available; use genuine saved output for readable historical terminal captures where accepted. |
| Prometheus Targets / Grafana | Real EKS original UI images inspected. Prometheus addresses remain private; the refreshed original Grafana screenshot was inspected with the corrected 0–100% axis. |
| Backend /metrics | Real application metrics were scraped and queried successfully; retain saved curl output, or label a separately performed local metric demonstration with its actual environment. |
| Pytest / Compose / non-root / security / GHCR / Git history | Actual source-pinned CI reports and historical original screenshots retained; use their exact run/source labels. Pinned complete baseline linked above; use the current source's own run and reports. |
| Deployment update / personal presentation | Prepared script and automatic kind/Flux evidence available; personal presentation pending, AWS Actions integration blocked. |
| Terraform destroy | Separate approval received; saved destroy-plan apply and all project residual checks passed. [Result](AWS-CLEANUP-VERIFICATION.md). Keep genuine private command logs for terminal-format evidence. |

Keep the full raw EKS archive and AWS Console images private unless disclosure is explicitly reviewed. Publish only the safe app captures and aggregate facts already identified. Do not substitute kind screenshots for real EKS evidence or an automated capture for a student's personal presentation.

## Suggested final walkthrough

1. Use an available local/CI environment for live app actions, and identify the real EKS captures as historical. Explain create/edit/stock adjustment, rejected overselling and retained ledger.
2. Show 44 PostgreSQL passes/97.67% coverage, Compose persistence, non-root runtimes, both Trivy reports and SHA-tagged GHCR images from the exact cited run.
3. Show the real AWS plan/VPC/subnets/EKS/group, Ready workers, two application replicas, Helm revision, ingress and HPA metrics.
4. Show the genuine saved Prometheus/Grafana captures; explain the completed and verified 0–100% error-axis correction.
5. Distinguish automatic kind/Flux deployment from manually bootstrapped EKS and disclose the OIDC-policy blocker.
6. Present or record personally. Include the actual separately approved cleanup result and retained database backup; a new paid AWS demo needs a new reviewed cost/runtime approval.

[Demo script](FINAL-DEMO-SCRIPT.md) · [Capture checklist](FINAL-PRESENTATION-CHECKLIST.md) · [Instructor Q&A](INSTRUCTOR-QA.md).

The original six-hour window ended on 18 October. Cleanup completed **05:16:28 IST on 22 October**, beyond that window. The US$10 target was not an automatic cutoff; actual charges and credits have not been checked. The verified result concerns the identified StockPilot resources.
