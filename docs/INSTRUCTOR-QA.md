# StockPilot instructor questions

Use these to rehearse your own understanding. Answers describe the implemented project and distinguish tested kind behavior from the unexecuted AWS lifecycle.

| Question | Concise answer |
|---|---|
| What problem does this app solve? | Small businesses can manage product balances and trace stock changes using a retained movement ledger, reorder alerts and an INR inventory dashboard. |
| What makes it your own application? | The domain, inventory workflow, original React dashboard, conditional stock adjustments and ledger are StockPilot features. The DevOps architecture follows course concepts. |
| What does React do? | It renders the interactive browser interface, validates user input and calls relative `/api` endpoints. Nginx serves the built assets. |
| Why FastAPI and PostgreSQL? | FastAPI exposes validated REST contracts; PostgreSQL persists relational records and provides transactional updates. |
| How is overselling prevented? | A database-side conditional arithmetic update requires enough remaining stock. The movement and balance commit together; conflicting excessive removal is rejected. |
| What survives deletion? | The movement ledger retains product name/SKU history after the product leaves the catalog. |
| Does inventory value mean profit? | No. It is quantity multiplied by selling price, in INR, not cost valuation or profit. |
| Why use Alembic? | Versioned migrations provide reviewable schema evolution. One migration Job runs per release rather than every replica migrating independently. |
| Are all 44 tests passing locally? | The cited CI run used PostgreSQL and passed all 44. The local SQLite fallback passed 43 and skipped the PostgreSQL concurrency case; it must not be described as 44 local passes. |
| How is the test DB isolated? | Fixtures provide an isolated test database; configured PostgreSQL test DB names must end in `_test`. Tests do not use production data. |
| What does coverage show? | The reviewed PostgreSQL run reports 97.67% executed Python statements. Coverage is not proof that all behaviors or security properties are correct. |
| What is Git versus GitHub? | Git records source history; GitHub hosts the repo and runs collaboration, Actions and GHCR services. A commit SHA identifies the source snapshot. |
| Why use a multistage Dockerfile? | The frontend build runs with Node, then copies assets into unprivileged Nginx. Build tools stay out of the serving runtime. |
| What does non-root mean here? | Backend runs as UID 10001 and frontend as UID 101. Dropped capabilities/read-only filesystems add defense, but non-root alone is not complete isolation. |
| Where does Compose data live? | PostgreSQL uses a named persistent volume; stopping/restarting containers keeps it. `down -v` explicitly deletes local demo data. |
| What fails the pipeline? | Failing tests, quality checks, secret scanning, HIGH/CRITICAL image findings or cluster acceptance prevent successful promotion. No security gate is bypassed. |
| What is the CVE example? | CVE-2026-76642 was reported against Debian util-linux-derived packages. We changed the runtime distribution and retested; see the detailed explanation rather than claiming a Debian package upgrade. |
| Why keep exact SHA image tags? | They trace source→scan→published image→deployment. The workflow loads the same scanned image tar for publishing. Tags alone are not cryptographic immutability; digest pinning is a further control. |
| What does Terraform create? | The proposed stack includes a two-AZ VPC, two public and two private subnets, IGW/NAT/routes, EKS, two managed workers, IAM/access entries, EBS CSI and logs. Real provisioning remains blocked on account access/approval. |
| What does a mock Terraform test prove? | Configuration/topology assertions with synthetic provider data. It does not prove account access, regional quotas, an actual plan or resource creation/deletion. |
| Why private workers and restricted API access? | Workers need no public IPs and use NAT for egress; the API permits private access plus approved public CIDRs. IAM/OIDC authentication does not bypass network restrictions. |
| Why one NAT? | It reduces demo cost, with a single-AZ failure dependency and possible cross-AZ transfer costs. Production reliability may require a different network design. |
| Why use OIDC? | A narrowly trusted GitHub production job assumes a temporary AWS role instead of storing permanent AWS keys. The role is namespace-scoped for app updates, not cluster bootstrap. |
| What is EKS versus kind? | EKS is AWS's managed Kubernetes control plane. kind runs real Kubernetes in Docker for disposable validation. kind does not earn proof of AWS VPC/EKS provisioning. |
| Deployment versus Service versus Ingress? | Deployment reconciles replicas; Service selects Pods with stable networking; Ingress describes HTTP routes implemented by Traefik. |
| Does `/health` through frontend prove backend liveness? | No. Ingress routes `/api` to backend and `/` to frontend. Check backend health/readiness through its Service/port-forward; verify `/api` through actual Ingress. |
| Why do migration Pods show Completed? | They are finite Jobs. Application/database Pods must be Running and Ready; a successful migration Pod should complete. |
| What does Helm rollback restore? | Application manifests and images. Database changes require a separate compatible migration/restore plan. |
| Why is the PVC still present after uninstall? | StatefulSet claims deliberately survive release deletion to protect data. Delete the exact disposable claim only after backup/evidence and explicit data-loss approval. |
| Why can the HPA remain at two replicas? | It responds to CPU utilization relative to requests. Low CPU legitimately keeps the minimum; metrics must be available, and scale-out should only be claimed if observed. |
| HPA metrics versus Prometheus? | metrics-server supplies CPU/resource metrics to HPA. Prometheus scrapes application counters/histograms for monitoring; Grafana queries them. |
| What does p95 latency mean? | An approximate latency below which 95% of observed requests fall, calculated from histogram bucket rates across replicas. |
| Why can a graph show startup errors? | They are part of the real history. Preserve them, check current health, and explain the event; do not edit the screenshot to hide it. |
| What did Flux actually do? | In CI it fetched the tested source SHA and reconciled the committed HelmRelease, upgrading to revision 2 and rolling APP_ENV to `gitops-ci`. |
| Can Flux and Actions both own the release? | They should not independently reconcile the same release. Production Flux is suspended when Actions owns EKS deployment; CI deliberately hands ownership over in its disposable cluster. |
| How do you debug an empty Service? | Compare selector and Pod labels, inspect EndpointSlices and Pod readiness, fix the actual mismatch, then verify endpoints and HTTP behavior. |
| How do you debug ImagePullBackOff? | Read Pod events, verify repository/tag/access and architecture, repair the cause and observe a Ready Pod. Deleting the Pod alone does not fix it. |
| How do you prevent surprise AWS costs? | Agree on account, rates, duration and budget before provisioning; save evidence, separately authorize teardown, remove LBs/PVCs, destroy Terraform resources and check for residual costs. |
| What remains before full completion? | Real AWS plan/VPC/EKS and runtime have executed evidence. The audit now covers 92 technical points; two cleanup points still need separate approval and actual destroy, four points need the student's explanation/presentation, and two form points are intentionally excluded. Literal Console/terminal captures remain format follow-up. Automatic AWS Actions deployment is separately blocked by account OIDC policy. These are evidence categories, not awarded marks. |
| What would production require? | Authentication/authorization, TLS, managed HA database/backups, tested restores, persistent monitoring, stronger network/IAM controls and operational ownership. The capstone is a demonstration, not a production certification. |

Architecture and tool responsibilities: [ARCHITECTURE.md](ARCHITECTURE.md). Exact execution and cleanup steps: [DEPLOYMENT.md](DEPLOYMENT.md). Actual evidence: [EVIDENCE.md](EVIDENCE.md).
