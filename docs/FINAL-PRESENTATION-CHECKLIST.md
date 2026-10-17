# Final presentation and capture checklist

This is a preparation checklist, not a claim that a personal presentation or AWS lifecycle has occurred. Form submission: **Student action — excluded from this task.** Do not open, populate or submit the official form through this workflow.

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
| Browser app | URL, dashboard, create/edit/adjust, mobile usability | Genuine CI screenshots available; live narrated demonstration remains student work. |
| Database/persistence | Product identity before/after actual DB restart in disposable Compose | Actual CI persistence output available; capture terminal for strict screenshot format. |
| Pytest | Command, all 44 PostgreSQL passes, coverage and test DB context | Reviewed CI transcript available; local SQLite is 43 passes plus one skipped concurrency test. |
| Containers | Both non-root Dockerfiles; healthy Compose and completed migration | Actual build/health evidence available; literal terminal capture if requested. |
| Git and pipeline | Ten meaningful commits; new real commit SHA; its green run | Existing history/run evidence available; record the new sequence personally. |
| Security | Both image reports and enforced HIGH/CRITICAL gate | Actual reports available; explain clean results and earlier CVE accurately. |
| Registry | Both package pages with the same source SHA | Reviewed public pull receipts available; check the demo SHA after its run. |
| Deployment change | Before/after images, Helm revision, new UI, successful deployment | Automated kind/Flux proof available; EKS job remains blocked/skipped. |
| AWS | Region, VPC, two public subnet AZs/routes, EKS ACTIVE, managed group ACTIVE | Blocked: no authenticated AWS account in this workspace. |
| Kubernetes | Ready nodes; Running Pods, two frontend/backend replicas, Services and Ingress; Helm list | Actual kind evidence available; EKS proof must be captured on EKS. |
| HPA | CPU metrics present, ScalingActive=True; scale-out only if observed | Kind evidence available; verify EKS separately. |
| Monitoring | Curl metrics, actual UP targets, populated request-rate/latency charts | Genuine kind screenshots available; capture EKS only after EKS execution. |
| Troubleshooting | Selector vs labels/EndpointSlices, image-pull event, fix and retest | Genuine isolated CI investigations available. |
| Cleanup | Reviewed teardown scope; actual destroy completion, empty state and residual-resource checks | Blocked until actual provisioning, evidence collection and separate teardown approval. |

## Before finishing

- [ ] Watch the complete recording and verify audio/legibility, source/cluster labels and the observed deployment update.
- [ ] Check every public file for credentials, passwords and sensitive identifiers. Redaction must not change finding severity, counts or outcomes.
- [ ] Save cloud/app/video evidence before any destructive cleanup.
- [ ] Obtain explicit approval for the exact disposable AWS teardown; remove demo LoadBalancers/PVCs first and check for residual charges afterward.
- [ ] Update actual results in `rubric-audit.json`, regenerate `RUBRIC-CHECKLIST.md`, and preserve immutable evidence links. Do not mark rehearsed explanations or unaccepted videos as VERIFIED.
- [ ] Keep the official form marked **Student action — excluded from this task.**
