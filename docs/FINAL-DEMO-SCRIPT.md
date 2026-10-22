# Timed presenter script

[Documentation hub](README.md) · [PowerPoint/notes](presentation/README.md) · [Capture checklist](FINAL-PRESENTATION-CHECKLIST.md) · [Recording chapters](demo/README.md)

Target 10–15 minutes of speaking. A fresh full pipeline can take longer. Use architecture/security discussion during waits, or transparently edit waiting time only if the instructor accepts a recorded walkthrough. **No student recording is claimed here.**

## Preparation

Use an available local Compose or kind environment and synthetic products. The real AWS EKS environment was captured historically and deleted after approval. Its optional Actions deployment job stayed disabled by account OIDC policy. Install the deck's fonts if needed and rehearse the notes.

## Speaking plan

| Time | Demonstration | Explain |
|---|---|---|
| 0:00–1:00 | Introduce StockPilot and the dashboard | Unique SKUs, dependable stock, retained history and database-derived statistics |
| 1:00–3:00 | Create six units, edit details, remove four, reject removal of 99, delete and inspect history | Conditional SQL, atomic balance/movement transaction, 409 conflicts and snapshots |
| 3:00–4:30 | Open Swagger, schema and test output | FastAPI validation, Alembic ownership, separate `_test` PostgreSQL database, 44 passes and 97.67% coverage in the pinned baseline |
| 4:30–6:00 | Show Dockerfiles/Compose and non-root runtime proof | Migration ordering, named database storage, UID 10001/101 and persistence after restart |
| 6:00–8:00 | Make a meaningful commit and follow its actual Actions run | Quality, Compose, scans, exact SHA image promotion and a real failure stopping publication |
| 8:00–9:30 | Explain the actual libx11 CVE/fix, inspect original scan reports and GHCR receipts | The unchanged HIGH/CRITICAL gate and point-in-time scan limits |
| 9:30–11:30 | Inspect Helm/Pods/Services/ingress/HPA and monitoring in the chosen runtime | Two application replicas, CPU input versus Prometheus, real UP targets and populated panels |
| 11:30–13:00 | Observe the actual Flux update and show the historical AWS lifecycle | Source SHA, Ready Helm revision 2, manual EKS distinction, captured Sydney architecture and approved cleanup |
| 13:00–15:00 | Summarize tradeoffs and answer questions | Single DB/NAT, authentication/TLS/recovery limits, personal assessment and exact remaining formats |

The table is a planned speaking sequence, not timestamps in an existing video. An interrupted/failed new run must be described accurately until repaired.

## A genuine commit and deployment update

1. Choose a small meaningful, visible change you understand in an available permitted environment. Do not recommit unmodified files just for a screenshot.
2. Explain the diff, commit it and push to the intended branch using the normal gated process.
3. Open that exact Actions run and inspect its tested source SHA. Do not substitute a different run's green status.
4. After image scans/publication, inspect the actual Kubernetes/Flux receipt and observed configuration/release revision for the same SHA. CI kind is disposable and removed at job completion; show its genuine archived receipt if the runner has already cleaned up.
5. If presenting a local kind environment separately, label its local release/update explicitly. A local Helm update is not a claim of successful AWS Actions deployment.

The existing [application baseline](https://github.com/not-so-shubh/devops-project/actions/runs/39696800574) and [Flux receipt](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/gitops-ci.json) show the technical chain. They do not prove that the student has personally demonstrated it.

## Historical AWS explanation

Show genuine saved VPC/EKS/managed-worker captures from Sydney on 18 October and explain the two public/two private subnets, two Ready workers and Bound 5 GiB gp3 database. Then show the [approved cleanup receipt](AWS-CLEANUP-VERIFICATION.md) at 05:16:28 IST on 22 October: 33 Terraform resources, two workers, three EBS disks and project residuals gone.

The operator applied a saved destruction plan. Do not claim a different literal command or that the deleted ingress endpoint is still available. Actual billing totals/credits remain unverified. If Console screenshots were never saved, state the format gap honestly.

## Recording and questions

Check audio/legibility, hide passwords/private account identifiers and retain exact source labels. Use [the 14-chapter guide](demo/README.md) when a real video is available. [Trivy preparation](TRIVY-EXPLANATION.md) and [instructor questions](INSTRUCTOR-QA.md) support rehearsal; personal understanding is assessed by the instructor.

Official form: **Student action — excluded from this task**.
