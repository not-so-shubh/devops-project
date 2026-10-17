# StockPilot: final demonstration script

Target: 10–15 minutes of presentation, with pipeline waiting time edited transparently in an accepted recording or filled by architecture/security discussion. A complete pipeline takes longer than the speaking time: do not promise a 15-minute uninterrupted run including AWS provisioning. No accepted student recording has been produced in this session. All existing cluster screenshots are from disposable **kind**, not AWS EKS.

Use [the presentation checklist](FINAL-PRESENTATION-CHECKLIST.md) to prepare. Read [Trivy explanation](TRIVY-EXPLANATION.md) and [instructor Q&A](INSTRUCTOR-QA.md). The official form is **Student action — excluded from this task.**

## 12-minute speaking plan

| Time | Say and demonstrate | Actual evidence/check |
|---|---|---|
| 0:00–0:40 | “StockPilot helps a small business track inventory and understand why stock changed. It is my inventory application, with a React interface, FastAPI and PostgreSQL.” | Dashboard, responsive layout, navigation; distinguish original app from the reference TaskBoard domain. |
| 0:40–2:20 | Add unique SKU `DEMO-LAMP-<date>`, opening quantity 6, threshold 3. Edit its name or price. Remove 4 with reason “Demo customer order.” Try removing 99. | Balance 2; low-stock status; rejection without an incorrect ledger entry; movement history. Open the quick guide and explain the overselling rule. |
| 2:20–3:00 | “The database keeps data outside the application process, and Alembic versions its schema.” Show product and ledger rows, restart PostgreSQL in the disposable Compose demo, then reopen the product. | `docker compose exec postgres psql -U stockpilot -d stockpilot -c 'SELECT sku, stock_quantity FROM products;'`; follow [persistence verifier](../scripts/verify-compose-persistence.py). Do not restart an unrelated database. |
| 3:00–4:00 | Show Swagger, health, readiness and `/metrics`; explain GET/POST/PUT/DELETE and validation. | Local backend `/docs`; `/health` proves liveness, `/ready` checks DB/schema; Ingress forwards `/api` without rewriting. Health/metrics are directly available on backend port-forward, not necessarily the frontend `/health` URL. |
| 4:00–5:00 | Show 44 real PostgreSQL test passes and 97.67% coverage from the cited reviewed run. Show isolated test DB and Dockerfiles. | Tests run before builds; backend UID 10001; frontend UID 101 and Node→Nginx stages; Compose services healthy and migration service completed. A local SQLite run may skip the PostgreSQL concurrency test: disclose it. |
| 5:00–6:00 | Make a useful, small UI wording change you can explain. Review its diff, lint/build, commit descriptively and push. | Capture old screen, old SHA and new SHA. Use the exact commit later when checking GHCR and Kubernetes images. The quick-guide overselling clarification is a real example in this task; do not make empty commits. |
| 6:00–7:30 | Follow Actions quality→Compose→build/scans→publish→cluster validation. Explain the original blocked Debian scan and maintained-runtime fix. | Use the actual new run, not a prior green screenshot. Show both reports and both SHA image tags. During build waiting time discuss tools/security rather than pretending the pipeline already finished. |
| 7:30–9:00 | Show Pods, Services, Helm, Ingress and HPA. Compare the image before/after deployment and reload the changed quick guide. | Commands below; require a successful deployment job for EKS. For the verified kind fallback, identify the cluster as disposable CI Kubernetes; source, tag and Flux revision must match. |
| 9:00–10:00 | Show Prometheus UP targets and a populated Grafana chart after safe traffic. | Request counter, rate and p95 latency; HPA uses metrics-server CPU, not this Prometheus dashboard. Only claim scale-out if observed. |
| 10:00–11:00 | Explain actual Terraform architecture and show real AWS evidence only if captured. | VPC ID, two public subnets in separate AZs, private workers, EKS ACTIVE, node group ACTIVE and Ready nodes. Without AWS access say explicitly that these 11 rubric points remain blocked. |
| 11:00–12:00 | Explain controlled troubleshooting and cleanup. | Actual selector/EndpointSlice and image-pull investigation; repaired endpoint counts and Pod logs. Capture cloud/demo evidence first; authorize teardown separately; show actual destroy and residual checks only after execution. |

## Commit and deployment sequence

For a local demonstration first confirm the working branch and destination. Keep credentials and `.env` out of the diff. A push to main starts the full pipeline; if AWS deployment is enabled it also updates the paid cluster and requires existing cost/deployment authorization.

```bash
git status --short
git log -10 --oneline
git diff -- frontend/src/main.jsx
npm --prefix frontend run lint
npm --prefix frontend run build
git add frontend/src/main.jsx
git commit -m "docs(ui): clarify inventory adjustment guidance"
git push origin main
git rev-parse HEAD
```

Choose a meaningful change appropriate to the final source; do not repeat the already implemented sentence just to manufacture another commit. Watch that commit's run to completion. Check both published SHA images. The automated CI kind deployment and Flux reconciliation are reproducible technical evidence; they do not substitute for your personal presentation or for an AWS deployment job.

On an authorized connected EKS cluster, with CI ownership active and Flux suspended for this release:

```bash
kubectl config current-context
kubectl get nodes
kubectl get pods,deployments,services,ingress,hpa -n stockpilot
kubectl get deployment stockpilot-backend stockpilot-frontend -n stockpilot \
  -o custom-columns='NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image,READY:.status.readyReplicas'
helm list -n stockpilot
helm history stockpilot -n stockpilot
kubectl top pods -n stockpilot
```

Record the original images and Helm revision before pushing, then the new SHA images, rollout completion and higher release revision after the deployment job succeeds. Open the actual Ingress hostname and show the changed UI. Do not use a localhost port-forward as proof of direct public load-balancer access. Follow [DEPLOYMENT.md](DEPLOYMENT.md) for DNS/Host routing and controller forwarding. App records in Compose and Kubernetes are separate databases.

## Three-minute shortened version

1. **0:00–0:45:** Show dashboard, create/edit product, adjust stock, demonstrate rejection and retained history.
2. **0:45–1:30:** Show actual test output, non-root builds, blocked-then-fixed Trivy history and both successful SHA images.
3. **1:30–2:15:** Show the real new commit, its completed run, deployed image SHA, Helm revision and changed UI. A recording may jump over the wait with explicit timestamps; retain full logs.
4. **2:15–3:00:** Show Running Pods, Ingress/HPA, UP targets/Grafana; show genuine AWS/destroy evidence if available and state outstanding items accurately.

## Recording and evidence rules

Use your operating system's screen recorder with microphone if the instructor accepts remote walkthroughs. Capture browser URL bars, terminal commands and results, run URLs, timestamps, commit SHAs and cluster context. Pause before password prompts, SSO/credential pages and Secret retrieval. Never film tokens, kubeconfig, database URLs or Secret YAML. Resume after authentication. Save the unedited recording privately; publish only a reviewed copy with no secrets. Screen recordings are not automatically accepted merely because they exist: confirm the course's presentation format yourself.

Before cleanup play back the recording and confirm the required screens and audio are legible. Save command output and cloud screenshots independently. If a live cluster is required on presentation day, agree on the cost of keeping it versus recreating it; never silently destroy it early or leave it running indefinitely.
