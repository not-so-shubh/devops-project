# Final presentation and capture checklist

## Verified AWS lifecycle — 22 October 2026

The real Sydney EKS demo was provisioned, exercised and captured on 18 October. After separate explicit approval, cleanup completed at **05:16:28 IST on 22 October**: **33 Terraform resources destroyed**, two workers terminated, three EBS disks and the ingress load balancer deleted, NAT/Elastic IP/VPC/project roles/log group absent, and Terraform state empty. The database backup was downloaded and its uploaded checksum matched. [Cleanup evidence](AWS-CLEANUP-VERIFICATION.md) · [Historical EKS captures](AWS-EKS-CAPTURE-REVIEW.md).

The audit records **43 VERIFIED criteria / 94 technical points**, **4 READY FOR DEMO points** for the student's explanation/presentation, and **2 EXCLUDED form points**. These are evidence totals, not awarded marks. Supply any Console screenshots already saved and retain genuine terminal transcripts; deleted AWS Console pages cannot be recreated as authentic screenshots from CLI JSON.

[The pinned completed baseline CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39117229787) includes tests, security scans, publication and kind/Flux validation. Later sources have their own [Actions results](https://github.com/not-so-shubh/devops-project/actions/workflows/ci-cd.yml) and `evidence/<source-sha>` reports. A subsequent libx11 security failure and package remediation are recorded in [the security explanation](TRIVY-EXPLANATION.md); publication remains gated by HIGH/CRITICAL scans.

Automatic EKS deployment remains disabled because account policy blocked OIDC-provider access. Use a permitted local/CI environment for a new personal demonstration and label it accurately; a new paid AWS environment requires a new reviewed cost/runtime approval. Official form: **Student action — excluded from this task**.
This checklist distinguishes prepared personal presentation steps from the now-executed AWS provisioning/runtime evidence. Final destroy is verified; the student's personal presentation remains outstanding. Form submission: **Student action — excluded from this task.** Do not open, populate or submit the official form through this workflow.

## Before recording

- [ ] Rehearse [FINAL-DEMO-SCRIPT.md](FINAL-DEMO-SCRIPT.md), [TRIVY-EXPLANATION.md](TRIVY-EXPLANATION.md), and [INSTRUCTOR-QA.md](INSTRUCTOR-QA.md).
- [ ] Confirm the exact main SHA and its latest successful run; read that run's `ci-run.json` on `evidence/<sha>` and check individual job results.
- [ ] Select Compose, local kind or authorized EKS; label every screenshot with the environment. CI kind is deleted after each run.
- [ ] For local kind, install Docker/kind/Helm/kubectl and run `bash scripts/local-kind.sh`; allocate at least 8 GB. Confirm that your chosen machine has a working Docker daemon.
- [ ] For EKS, complete [AWS-READINESS.md](AWS-READINESS.md), account authentication, cost/plan approval, provisioning and bootstrap. Confirm API connectivity and registry pulls.
- [ ] Test microphone, terminal font and browser zoom. Close credential tabs and disable notifications. Check passwords are not visible in shell history or screenshots.
- [ ] Keep app, API docs, Actions, GHCR, Prometheus, Grafana and the rubric ready. Prepare a distinct demo SKU and safe test data.
- [ ] Record old image tags/Helm revision before the useful commit. Confirm whether CI or Flux owns the release; never let both reconcile it independently.

## Required captures

| Capture | Include | Current state |
|---|---|---|
| Browser app | URL, dashboard, create/edit/adjust, mobile usability | Genuine real EKS desktop/mobile/dialog screenshots inspected; live narrated demonstration remains student work. |
| Database/persistence | Product identity before/after actual DB restart in disposable Compose | Actual CI persistence output available; capture terminal for strict screenshot format. |
| Pytest | Command, all 44 PostgreSQL passes, coverage and test DB context | Reviewed CI transcript available; local SQLite is 43 passes plus one skipped concurrency test. |
| Containers | Both non-root Dockerfiles; healthy Compose and completed migration | Actual build/health evidence available; literal terminal capture if requested. |
| Git and pipeline | Ten meaningful commits; new real commit SHA; its green run | Existing history/run evidence available; record the new sequence personally. |
| Security | Both image reports and enforced HIGH/CRITICAL gate | Actual reports available; explain clean results and earlier CVE accurately. |
| Registry | Both package pages with the same source SHA | Reviewed public pull receipts available; check the demo SHA after its run. |
| Deployment change | Before/after images, Helm revision, new UI, successful deployment | Automated kind/Flux proof available; EKS job remains blocked/skipped. |
| AWS | Region, VPC, two public subnet AZs/routes, EKS ACTIVE, managed group ACTIVE | Real CloudShell plan/VPC/subnet/routes/EKS/group/Ready-node outputs inspected; literal AWS Console screenshots still pending. |
| Kubernetes | Ready nodes; Running Pods, two frontend/backend replicas, Services and Ingress; Helm list | Actual EKS workloads, Services, ingress, Helm and Ready-node outputs inspected; preserve literal terminal screenshots. |
| HPA | CPU metrics present, ScalingActive=True; scale-out only if observed | Actual EKS CPU metrics confirmed; HPA at 3–4% against 65% with two replicas. No scale-out claimed. |
| Monitoring | Curl metrics, actual UP targets, populated request-rate/latency charts | Real EKS Targets and authenticated populated Grafana screenshots inspected; refresh the error-axis fix capture and collect literal curl output. |
| Troubleshooting | Selector vs labels/EndpointSlices, image-pull event, fix and retest | Genuine isolated CI investigations available. |
| Cleanup | Reviewed teardown scope; actual destroy completion, empty state and residual-resource checks | Completed after separate approval; 33 Terraform deletes, empty state and AWS residual checks passed. See AWS-CLEANUP-VERIFICATION.md. |

## Before finishing

- [ ] Watch the complete recording and verify audio/legibility, source/cluster labels and the observed deployment update.
- [ ] Check every public file for credentials, passwords and sensitive identifiers. Redaction must not change finding severity, counts or outcomes.
- [ ] Save cloud/app/video evidence before any destructive cleanup.
- [x] Separate teardown approval received; demo LB/PVC removed, saved destroy plan applied and project residual checks passed. Actual billing totals/credits remain unverified.
- [ ] Update actual results in `rubric-audit.json`, regenerate `RUBRIC-CHECKLIST.md`, and preserve immutable evidence links. Do not mark rehearsed explanations or unaccepted videos as VERIFIED.
- [ ] Keep the official form marked **Student action — excluded from this task.**
