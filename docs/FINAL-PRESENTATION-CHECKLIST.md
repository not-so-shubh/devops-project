# Final presentation and capture checklist

## Real AWS status — 18 October 2026

Real StockPilot EKS deployment in **Sydney (ap-southeast-2)** is now verified: two Ready workers, two backend and two frontend replicas, a Bound 5 GiB gp3 database, passed HTTP smoke and all four desktop/mobile browser scenarios. Real Prometheus targets and an authenticated populated Grafana dashboard were captured and visually inspected. [Reviewed EKS evidence](AWS-EKS-CAPTURE-REVIEW.md) distinguishes deployed application source `84c18de84538a74a8bab92b89dc72d6e89a393d0` from capture-tool source `cf87b82b40151d0c21c2e03740451a1a9ed2c649`.

The [latest fully reviewed CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39115536536) is green, including tests, scans, publication and real kind/Flux validation. AWS Actions deployment remains disabled/skipped: organization policy denied OIDC listing and a targeted provider lookup also failed. Manual EKS deployment is verified; automatic GitHub-to-EKS deployment is not.

The audit supports **92 technical points**, with **4 student explanation/demo points**, **2 cleanup points** and **2 excluded form points** outstanding. Literal AWS Console/terminal screenshot formats also require collection. Final teardown needs separate reviewed approval. The original approved runtime ends **17:12:07 IST on 18 October 2026**; recovery did not reset that window.

This checklist distinguishes prepared personal presentation steps from the now-executed AWS provisioning/runtime evidence. Final destroy and personal presentation have not occurred. Form submission: **Student action — excluded from this task.** Do not open, populate or submit the official form through this workflow.

## Before recording

- [ ] Rehearse [FINAL-DEMO-SCRIPT.md](FINAL-DEMO-SCRIPT.md), [TRIVY-EXPLANATION.md](TRIVY-EXPLANATION.md), and [INSTRUCTOR-QA.md](INSTRUCTOR-QA.md).
- [ ] Confirm the exact main SHA and its latest successful run; read that run's `ci-run.json` on `evidence/<sha>` and check individual job results.
- [ ] Select Compose, local kind or authorized EKS; label every screenshot with the environment. CI kind is deleted after each run.
- [ ] For local kind, install Docker/kind/Helm/kubectl and run `bash scripts/local-kind.sh`; allocate at least 8 GB. This workspace lacks a Docker daemon and cannot host that environment.
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
| Cleanup | Reviewed teardown scope; actual destroy completion, empty state and residual-resource checks | Pending exact teardown review, saved demo/backup and separate approval; no final destroy performed. |

## Before finishing

- [ ] Watch the complete recording and verify audio/legibility, source/cluster labels and the observed deployment update.
- [ ] Check every public file for credentials, passwords and sensitive identifiers. Redaction must not change finding severity, counts or outcomes.
- [ ] Save cloud/app/video evidence before any destructive cleanup.
- [ ] Obtain explicit approval for the exact disposable AWS teardown; remove demo LoadBalancers/PVCs first and check for residual charges afterward.
- [ ] Update actual results in `rubric-audit.json`, regenerate `RUBRIC-CHECKLIST.md`, and preserve immutable evidence links. Do not mark rehearsed explanations or unaccepted videos as VERIFIED.
- [ ] Keep the official form marked **Student action — excluded from this task.**
