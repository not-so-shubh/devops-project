# Submission status and remaining work

Repository: https://github.com/not-so-shubh/devops-project

The latest fully reviewed successful CI source is `cf87b82b40151d0c21c2e03740451a1a9ed2c649`: [run 39115536536](https://github.com/not-so-shubh/devops-project/actions/runs/39115536536), with [durable CI evidence](https://github.com/not-so-shubh/devops-project/tree/405b839cd453bff6086a33b1f3ce4e68c19b3384/docs/evidence). Real EKS application source is `84c18de84538a74a8bab92b89dc72d6e89a393d0`. [The inspected EKS archive review](AWS-EKS-CAPTURE-REVIEW.md) records exact provenance and original-file hashes.

## Evidence-backed status

All 46 official criteria are listed in [RUBRIC-CHECKLIST.md](RUBRIC-CHECKLIST.md). There are **42 VERIFIED criteria / 92 technical points**, **4 READY FOR DEMO points**, **2 BLOCKED cleanup points**, and **2 EXCLUDED form points**. This is evidence coverage, not an awarded grade.

Real provider-backed Terraform plan, VPC with two public/two private subnets across two AZs, active routing, EKS and managed workers are executed and independently reviewed. Two workers are Ready. Real EKS Helm/PVC/replicas/ingress/HPA, four desktop/mobile browser scenarios, Prometheus UP targets and authenticated populated Grafana have actual proof.

| Remaining criterion | Points | Required completion |
|---|---:|---|
| M3.1 | 2 | **Student action — excluded from this task.** No official form opened, populated or submitted. |
| M6.3 | 1 | Personally explain the real Trivy result and limits using [TRIVY-EXPLANATION.md](TRIVY-EXPLANATION.md). Written preparation is complete; personal understanding has not been assessed. |
| M7.6 | 2 | After saving screenshots/recording/backup, review exact teardown scope, obtain separate explicit approval, remove the demo load balancer/database volume, execute Terraform destroy and verify residuals. |
| M10.2 | 3 | Personally present live or produce an accepted remote recording of a genuine commit → green CI → observed deployment update. Automatic kind/Flux and manual real EKS proof are distinct. |

The mission's additional automatic AWS deployment requirement is **BLOCKED**: organization policy explicitly denied OIDC-provider listing and the exact-provider lookup also returned AccessDenied. GitHub administrator access and login succeeded. The AWS deploy job remains disabled/skipped. A permitted account-policy configuration is required; manual EKS deployment does not close that gap.

## Required screenshot and recording formats

| Requested item | Current proof / next action |
|---|---|
| Running app, desktop/mobile | Original real EKS screenshots inspected and linked in [capture review](AWS-EKS-CAPTURE-REVIEW.md). |
| Terraform non-empty plan | Actual 33-create plan and private original transcript available; retain/capture the literal terminal image. |
| AWS Console VPC / EKS | Real CLI/API resources verified. Capture the Console pages in Sydney, showing VPC/subnets and EKS/group status, and keep account identifiers private. |
| Ready workers / Pods / Services / Helm list | Genuine private EKS output archive available; capture readable terminal screenshots to satisfy the exact requested format. |
| Prometheus Targets / Grafana | Real EKS original UI images inspected. Prometheus addresses remain private; refresh the Grafana screenshot after applying its error-axis display fix. |
| Backend /metrics | Real application metrics were scraped and queried successfully; capture literal curl output through a backend port-forward. |
| Pytest / Compose / non-root / security / GHCR / Git history | Actual source-pinned CI reports and historical original screenshots retained; use their exact run/source labels. Current complete green run linked above. |
| Deployment update / personal presentation | Prepared script and automatic kind/Flux evidence available; personal presentation pending, AWS Actions integration blocked. |
| Terraform destroy | Not executed or approved. Save actual completion and AWS residual checks after authorized cleanup. |

Keep the full raw EKS archive and AWS Console images private unless disclosure is explicitly reviewed. Publish only the safe app captures and aggregate facts already identified. Do not substitute kind screenshots for real EKS evidence or an automated capture for a student's personal presentation.

## Suggested final walkthrough

1. Show the real EKS app and create/edit/adjust a distinct demo product; explain rejected overselling and retained ledger.
2. Show 44 PostgreSQL passes/97.67% coverage, Compose persistence, non-root runtimes, both Trivy reports and SHA-tagged GHCR images from the exact cited run.
3. Show the real AWS plan/VPC/subnets/EKS/group, Ready workers, two application replicas, Helm revision, ingress and HPA metrics.
4. Show real Prometheus targets and Grafana request/latency data. Explain and apply the genuine error-axis fix accurately.
5. Distinguish automatic kind/Flux deployment from manually bootstrapped EKS and disclose the OIDC-policy blocker.
6. Present or record personally, save the evidence and backup, then review/approve final cleanup and retain genuine destroy results.

[Demo script](FINAL-DEMO-SCRIPT.md) · [Capture checklist](FINAL-PRESENTATION-CHECKLIST.md) · [Instructor Q&A](INSTRUCTOR-QA.md).

The original approved six-hour window ends **17:12:07 IST on 18 October 2026**. The US$10 target is not a hard cap; resources continue billing until deleted. Recovery did not reset the runtime window.
