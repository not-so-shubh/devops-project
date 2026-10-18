# StockPilot final demonstration

## Real AWS status — 18 October 2026

Real StockPilot EKS deployment in **Sydney (ap-southeast-2)** is now verified: two Ready workers, two backend and two frontend replicas, a Bound 5 GiB gp3 database, passed HTTP smoke and all four desktop/mobile browser scenarios. Real Prometheus targets and an authenticated populated Grafana dashboard were captured and visually inspected. [Reviewed EKS evidence](AWS-EKS-CAPTURE-REVIEW.md) distinguishes deployed application source `84c18de84538a74a8bab92b89dc72d6e89a393d0` from capture-tool source `cf87b82b40151d0c21c2e03740451a1a9ed2c649`.

The [latest fully reviewed CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39115536536) is green, including tests, scans, publication and real kind/Flux validation. AWS Actions deployment remains disabled/skipped: organization policy denied OIDC listing and a targeted provider lookup also failed. Manual EKS deployment is verified; automatic GitHub-to-EKS deployment is not.

The audit supports **92 technical points**, with **4 student explanation/demo points**, **2 cleanup points** and **2 excluded form points** outstanding. Literal AWS Console/terminal screenshot formats also require collection. Final teardown needs separate reviewed approval. The original approved runtime ends **17:12:07 IST on 18 October 2026**; recovery did not reset that window.

For a live remote walkthrough, show the real EKS environment and its saved evidence, then accurately distinguish automatic kind validation from the account-policy-blocked AWS deployment job. Do not present a manual Helm command as a successful AWS Actions deploy.

See [FINAL-DEMO-SCRIPT.md](FINAL-DEMO-SCRIPT.md) for the current preparation, evidence boundaries and remaining actions. Official form submission: **Student action — excluded from this task.**

Opening (20 seconds): “StockPilot helps a small business know what is on the shelf and why stock changed. I chose inventory operations rather than copying TaskBoard. The API uses PostgreSQL transactions, and the same application travels through tests, containers, a security gate, immutable registry images, Kubernetes, and monitoring.” Disclose implementation assistance according to your institution's policy and be ready to explain the submitted code yourself.

| Step | Demonstrate | Proof and explanation |
|---:|---|---|
| 1 | Open desktop dashboard, then mobile layout | Live count, INR inventory value, low stock, actual seven-day flow and categories; no invented growth percentages |
| 2 | Add a product with SKU `DEMO-LAMP`, quantity 6 and threshold 3 | Product form validation and opening movement; edit its name/price; inspect details |
| 3 | Remove 4 units with reason “Demo customer order”; try removing 99 | Balance becomes 2 and Low stock; 409 rejects excessive removal without an extra ledger row |
| 4 | Open Stock movements, then inspect PostgreSQL | `docker compose exec postgres psql -U stockpilot -d stockpilot -c 'SELECT sku, stock_quantity FROM products;'`; show `stock_movements` |
| 5 | Open localhost:8000/docs and /metrics | Explain REST status codes; liveness versus readiness; counter and histogram |
| 6 | Run `cd backend && pytest -v --cov=app --cov-report=term-missing` | Isolated database, real tests, PostgreSQL concurrency CI; do not present skipped tests as passed |
| 7 | Change the quick-guide wording or a CSS spacing value | Real, useful small change; run lint/build, `git diff`, `git add`, conventional commit and `git push origin main` |
| 8 | Open Actions and watch the new SHA | Explain dependency gates; show real quality, Compose and build/scan jobs |
| 9 | Show `docker images` / Dockerfiles | Non-root UIDs, Node→Nginx multi-stage, ports 8000/8080, read-only runtime, one-shot migrations |
| 10 | Open both Trivy job reports | OS/library scanning, HIGH/CRITICAL gate and actual result; explain a real finding or the limits of a clean report |
| 11 | Show GHCR packages and exact SHA tags | Trace source commit→tested/scanned image; demonstrate pull permissions |
| 12 | Show Terraform code, real plan, VPC and EKS console | Only claim actual provisioning after an approved apply; use recorded pending status otherwise |
| 13 | `kubectl get pods,svc,ingress,hpa -n stockpilot` | Two backend and frontend replicas, ready/running Pods and correct Service targets |
| 14 | `helm list -n stockpilot`, `helm history stockpilot -n stockpilot` | Reproducible chart and revision; show migration Job completion |
| 15 | Open app through actual Ingress hostname | `/` reaches frontend, `/api` reaches backend; no cluster-internal hostname in browser |
| 16 | Watch HPA and `kubectl top pods` while running load script | Requests define CPU utilization; metrics-server supplies CPU metrics; only claim scale-out if it occurs |
| 17 | Prometheus Targets and Grafana StockPilot dashboard | Target UP, request rate and latency populated after legitimate traffic; explain two scrape intervals |
| 18 | Isolated broken-Service exercise | Compare selector vs Pod labels, repair the lab Service and remove it; working app remains available |
| 19 | Explain and, when authorized, demonstrate cleanup | Capture AWS evidence first; remove LoadBalancers/PVCs then Terraform destroy; show completion and residual-resource check |

Finish by showing the evidence index and rubric checklist. A kind demonstration is real Kubernetes evidence, but it is not an AWS EKS provisioning claim. The live commit→pipeline→deployment update criterion remains pending until actually demonstrated in a configured environment. Save your own recording if the instructor accepts a remote walkthrough.

## Questions to rehearse

| Concept | Concise explanation |
|---|---|
| Git vs GitHub | Git stores version history; GitHub hosts it and runs collaboration/automation. A commit SHA identifies a source snapshot. |
| Why tests before images? | A failed behavior check stops promotion before registry/deployment work. PostgreSQL CI checks the actual database semantics. |
| Why a multi-stage image? | Build tooling stays in the builder; the runtime serves only built assets, reducing size and attack surface. |
| Why non-root? | A compromised process starts with fewer privileges; it still needs other controls and patched dependencies. |
| What does Trivy prove? | It matches the scanned image's OS/library inventory to known vulnerabilities at scan time. It does not prove absence of application flaws or future CVEs. |
| Why immutable SHA tags? | They connect deployed images to tested source. Rollback and audit are clearer than a mutable latest tag. |
| Terraform vs Kubernetes vs Helm | Terraform creates AWS resources; Kubernetes reconciles workloads; Helm packages/version-controls their configuration. |
| Deployment vs Service vs Ingress | Deployment manages replicas, Service gives stable Pod networking, Ingress implements external HTTP routing through a controller. |
| Liveness vs readiness | Liveness checks the running app; readiness verifies DB/schema access before accepting traffic. DB outages should not cause liveness restart storms. |
| Why Alembic? | Versioned/reviewable schema changes can be applied once per release; automatic table creation cannot manage controlled evolution. |
| Why atomic inventory updates? | A database-side conditional arithmetic update prevents two concurrent requests from both consuming the same units; the ledger commits with the balance. |
| HPA vs Prometheus | This HPA reads CPU via metrics-server; Prometheus provides application observation and dashboard data. |
| Histogram p95 | Bucket rates approximate the latency below which 95% of observations fall, aggregated across replicas. |
| Secret vs ConfigMap | Both are configuration objects; Secrets require stronger access/encryption controls. Base64 is encoding, not encryption. |
| OIDC | GitHub exchanges a narrowly trusted job identity for temporary AWS credentials, avoiding permanent AWS keys in GitHub. Network and EKS access are still required. |
| Helm rollback limitation | It restores application manifests/images; database rollback/restore is a separate, reviewed operation. |
| What remains for real production? | Authentication/authorization, TLS, managed HA database, tested backups, persistent monitoring, stronger network/IAM policies and operational ownership. |
