# StockPilot documentation

[Repository home](../README.md) · [Examiner handoff](FINAL-PROJECT-HANDOFF.md) · [Verified application CI](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574)

Start with the handoff for a short assessment route. The complete guides below distinguish local Compose, automatic disposable kind validation, and historical manual AWS EKS execution. The reviewed AWS resources were deleted after approval on 22 October 2026.

## Start here

- [Project overview and quick start](../README.md)
- [Final project handoff](FINAL-PROJECT-HANDOFF.md)
- [Submission status and exact outstanding actions](SUBMISSION.md)
- [Final polish file-by-file report](FINAL-POLISH-REPORT.md)

## Presentation and demo

- [Required root `demo/` submission folder](../demo/README.md) — deck and supplied MP4 present; video has no audio track

- [Presentation guide and speaker-note instructions](presentation/README.md)
- [Download the editable PowerPoint](../demo/StockPilot_Final_Presentation.pptx?raw=true)
- [Presentation preview](presentation/StockPilot_Presentation_Preview.png)
- [Demo recording guide and planned chapters](demo/README.md) — supplied recording linked; chapter plan remains unverified
- [Demonstration overview](DEMO.md)
- [Timed presenter script](FINAL-DEMO-SCRIPT.md)
- [Final presentation/capture checklist](FINAL-PRESENTATION-CHECKLIST.md)
- [Instructor questions](INSTRUCTOR-QA.md)

## Architecture and application

- [Architecture, data model and tradeoffs](ARCHITECTURE.md)
- [Backend setup and API contracts](../backend/README.md)
- [Frontend development and routing](../frontend/README.md)
- [Coursework application-directory mapping](../application/README.md)
- [Originality and attribution](../NOTICE.md)

## Development and testing

- [Testing, isolation, coverage and reproducible commands](TESTING.md)
- [Backend test source](../backend/tests/)
- [Playwright acceptance source](../e2e/)
- [Attached homework alignment and implementation lessons](HOMEWORK-ADDENDUM.md)

## Docker and CI/CD

- [Docker/Compose service guide](../docker/README.md)
- [Deployment environments and verification](DEPLOYMENT.md)
- [Actual workflow source](../.github/workflows/ci-cd.yml)
- [Current Actions runs](https://github.com/not-so-shubh/devops-project/actions/workflows/ci-cd.yml)
- [Source-pinned image receipts and CI evidence](EVIDENCE.md#source-pinned-ci-evidence)

## Security

- [Controls, gates, actual CVEs and repair history](../security/README.md)
- [Required written Trivy explanation and personal rehearsal](TRIVY-EXPLANATION.md)

## AWS and Terraform

- [Terraform scope, validation and operator boundaries](../terraform/README.md)
- [AWS readiness and historical execution](AWS-READINESS.md)
- [Historical EKS runtime verification](AWS-EKS-RUNTIME-VERIFICATION.md)
- [Original/refreshed capture review and hashes](AWS-EKS-CAPTURE-REVIEW.md)
- [Private capture procedure and CloudShell recovery history](AWS-EKS-CAPTURE.md)
- [Actual separately approved cleanup verification](AWS-CLEANUP-VERIFICATION.md)

## Kubernetes and GitOps

- [Kubernetes/Helm objects and environment-specific storage](../kubernetes/README.md)
- [Application Helm chart](../helm/stockpilot/)
- [Bootstrap manifests](../k8s/)
- [Flux reconciliation and release ownership](../gitops/README.md)
- [Local kind sequence](../scripts/local-kind.sh)

## Monitoring

- [Metric paths, discovery, dashboard queries and HPA](../monitoring/README.md)
- [Historical real EKS monitoring review](AWS-EKS-CAPTURE-REVIEW.md#refreshed-monitoring-capture)

## Troubleshooting

- [Symptoms, causes, diagnosis and verified fixes](TROUBLESHOOTING.md)
- [Isolated lab manifests](../troubleshooting/)
- [Source-pinned troubleshooting record](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/troubleshooting-ci.json)

## Evidence and grading

- [Evidence index, source map and historical chronology](EVIDENCE.md)
- [All 46 official criteria and point totals](RUBRIC-CHECKLIST.md)
- [Machine-readable maintained rubric audit](rubric-audit.json)
- [Actual cleanup receipt](evidence/aws-cleanup-summary.json)
- [Official instructor rubric](https://github.com/Nency-Ravaliya/devops-heros/blob/main/session21-python/GRADING.md)
- [Original project license](../LICENSE) and [retained reference license](../LICENSE.reference)

The audit's **94 verified technical points**, **4 personal-assessment points** and **2 excluded form points** are evidence categories, not awarded grades. The presentation file and recording guide do not complete the student's personal demonstration. Official form: **Student action — excluded from this task**.
