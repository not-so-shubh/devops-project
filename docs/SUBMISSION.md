# Submission status

[Documentation hub](README.md) · [Examiner handoff](FINAL-PROJECT-HANDOFF.md) · [Official rubric](https://github.com/Nency-Ravaliya/devops-heros/blob/main/session21-python/GRADING.md)

## Required submission media

The instructor’s follow-up requires **both the actual MP4 and the PPT/PDF in the root [`demo/` folder](../demo/README.md) of the same submitted repository**.

- [x] `demo/StockPilot_Final_Presentation.pptx`: actual editable deck present.
- [x] [demo/StockPilot_Final_Demo.mp4](../demo/StockPilot_Final_Demo.mp4?raw=true): supplied recording present; 11:00.56, 1920 × 1080, no audio track.

**Both required media files are present in `demo/`.** The supplied MP4 has no audio track. Its presence does not change the rubric audit or establish completion of a personal explanation or an instructor-accepted demonstration.

## Ready to evaluate

- [Original application and safe local setup](../README.md#quick-start).
- [Complete enabled application pipeline](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574), exact source `8944da7`, with [original receipts](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/ci-run.json).
- [Historical real AWS deployment/capture](AWS-EKS-CAPTURE-REVIEW.md) and [approved final cleanup](AWS-CLEANUP-VERIFICATION.md).
- [Editable final PowerPoint and preview](presentation/README.md), speaker notes, [timed script](FINAL-DEMO-SCRIPT.md) and [instructor Q&A](INSTRUCTOR-QA.md).
- [All 46 criteria](RUBRIC-CHECKLIST.md), totaling 100 available points.

The audit records **43 verified criteria / 94 technical points**, **2 criteria / 4 points READY FOR DEMO**, and **1 criterion / 2 points EXCLUDED**. These are evidence categories, not guaranteed or instructor-awarded grades. The presentation upload does not change these totals.

## Student actions still required

| Criterion | Points | Actual remaining action |
|---|---:|---|
| M6.3 | 1 | Personally explain a real CVE/clean scan and its limits using [Trivy preparation](TRIVY-EXPLANATION.md) |
| M10.2 | 3 | Personally perform a genuine commit → CI → observed deployment update, live or in a recording the instructor accepts |
| M3.1 | 2 | **Student action — excluded from this task.** Handle the official form independently |

**Recording status: supplied MP4 present in root `demo/`; no audio track.** Personal explanation and instructor acceptance remain to be assessed. [Recording chapters and file instructions](demo/README.md). A prepared deck or automated screenshot is not proof that the student's personal presentation occurred.

Automatic GitHub Actions deployment to EKS remains blocked by organization OIDC policy and was skipped. Real manual EKS deployment and automatic disposable kind/Flux reconciliation are separate verified paths. A personal demonstration can use an available permitted local/CI environment with accurate labels; a new paid AWS deployment is outside this handoff.

## Exact screenshot formats

| Requested format | Genuine source / next action |
|---|---|
| Running browser app | Public historical EKS desktop/mobile captures and source-pinned CI screenshots in [Evidence](EVIDENCE.md) |
| `pytest -v`, Compose, non-root and Trivy | Original run logs/reports and historical terminal images; save readable actual output in the requested format |
| Git history and GHCR SHA tags | Actual repository/package pages; preserve source labels and never call a failed run green |
| Terraform plan | Original 33-create CloudShell output and sanitized historical plan |
| AWS Console VPC/EKS in Sydney | Use genuine pre-deletion Console images already saved. The deleted environment cannot be recreated as authentic Console images from CLI JSON |
| Pods, Services, Helm list | Genuine saved EKS/CI terminal output, labelled by environment/date |
| `/metrics`, Prometheus Targets, Grafana | Original exposition, target and dashboard evidence; keep private EKS addresses out of public uploads |
| Destroy completion | Actual saved-plan application log, empty state and [scoped residual receipt](AWS-CLEANUP-VERIFICATION.md) |

Technical audit coverage does not certify that every exact screenshot format has been supplied. If a required Console image was never saved, report that gap honestly rather than fabricating a replacement or recreating paid infrastructure for this documentation task.

## Before the college presentation

1. Download the [PowerPoint](../demo/StockPilot_Final_Presentation.pptx?raw=true), open it locally and rehearse the notes.
2. Check your chosen Compose/kind environment, microphone and readable terminal/browser zoom.
3. Demonstrate the product and personal security explanation, then observe the actual commit/run/deployment chain.
4. Show historical AWS provisioning/runtime/cleanup with its original source/date, not as a current live endpoint.
5. Review the supplied `demo/StockPilot_Final_Demo.mp4` for chapter continuity and instructor acceptance; it has no audio track, so arrange any required spoken explanation.
6. Complete the official form yourself. **No official form was opened, populated or submitted in this work.**

The reviewed AWS resources are gone and the private database backup was retained. Cleanup finished beyond the original six-hour window; actual account charges/credits have not been checked.
