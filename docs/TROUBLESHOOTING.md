# Troubleshooting

Use observations to locate the failure before changing configuration. Keep the working release intact during the isolated lab.

| Symptom | Check | Corrective action |
|---|---|---|
| UI cannot fetch inventory | Browser Network tab, `curl localhost:8000/ready`, Compose backend logs | Start DB, run Alembic, confirm relative `/api`; do not strip `/api` in proxy |
| Product create returns 409 | Existing SKU; SKU normalization is uppercase | Use a unique SKU; do not disable the DB constraint |
| Adjustment returns 409 | Current balance and requested signed delta | Remove no more than available, or stay below 1,000,000; rejected writes add no movement |
| Compose DB password changed but connection fails | Existing named volume uses its original DB credentials | Restore correct password or intentionally recreate only demo data; changing `.env` does not reset an initialized database |
| API healthy but not ready | `/health` vs `/ready`, migration service/Job logs | Restore DB access, apply reviewed migrations; never replace production migrations with `create_all` |
| `ImagePullBackOff` | `kubectl describe pod`, image SHA and GHCR visibility | Confirm both packages/tag, public access or durable pull Secret; expired Actions tokens are unsuitable |
| Pending PostgreSQL PVC | `kubectl describe pvc`, `kubectl get storageclass`, EBS CSI addon and Pod Identity | Use `gp3` on EKS, `standard` in kind; confirm CSI role permissions and AZ placement |
| Helm waits until timeout | Pods/events and `kubectl logs job/stockpilot-migrate-N` | Verify DB Secret keys/URL, DNS, storage and migrations; only one concurrent upgrade |
| Ingress 404 | Host header, ingressClassName and controller | Use configured hostname; the resource alone is not an ingress controller |
| Ingress 502 / empty Service endpoints | Service selectors, EndpointSlices, container/Service ports | Frontend 8080, backend 8000; compare labels and named target port `http` |
| Nginx crashes as non-root | Logs, read-only filesystem and `/tmp` mount | Use unprivileged image, 8080 and writable temporary volume |
| HPA `<unknown>` | `kubectl top pods`, metrics APIService | Install healthy metrics-server; keep CPU requests; insecure kubelet TLS is only for disposable kind |
| Prometheus target absent | ServiceMonitor labels, namespace selector, Service labels/port | Match `release=monitoring`, app namespace label and Service `http` port |
| Prometheus target down | Curl backend `/metrics` from cluster, readiness/network | Fix reachable Service and route before changing dashboards |
| Grafana has no data | Prometheus query API, datasource UID `prometheus`, traffic and time range | Generate traffic; allow >=2 scrapes; inspect request metrics, not a hardcoded graph |
| Terraform provider cannot run locally | Executable/temp/socket permissions and recorded initialization logs | Use a normal Terraform host or CI validation; do not claim an AWS plan succeeded |
| EKS OIDC login succeeds but kubectl fails | Access entry, namespace scope, API network allowlist | IAM authentication, Kubernetes authorization, and network access are separate requirements |
| VPC destroy fails | Remaining Kubernetes LoadBalancers, ENIs, PVCs/volumes | Uninstall workloads/controller, delete authorized demo data, wait for external cleanup, then rerun plan/destroy |

## Controlled troubleshooting exercise

Use a demo cluster only:

```bash
kubectl apply -f troubleshooting/broken-service.yaml
kubectl get endpointslice -n stockpilot -l kubernetes.io/service-name=stockpilot-lab-empty-service
kubectl get pods -n stockpilot --show-labels
kubectl describe svc stockpilot-lab-empty-service -n stockpilot
```

Explain why no Pod matches the deliberate selector. Fix only the lab Service:

```bash
kubectl patch svc stockpilot-lab-empty-service -n stockpilot --type merge \
  -p '{"spec":{"selector":{"app.kubernetes.io/component":"backend","app.kubernetes.io/instance":"stockpilot"}}}'
kubectl get endpointslice -n stockpilot -l kubernetes.io/service-name=stockpilot-lab-empty-service
kubectl delete -f troubleshooting/broken-service.yaml
```

Optional image lab: apply `troubleshooting/broken-image.yaml`, inspect `kubectl describe pod` and events for the invalid tag, explain the pull failure, then `kubectl delete -f troubleshooting/broken-image.yaml`. Never break the live production Service or delete its database just to demonstrate diagnosis.

The disposable Kubernetes CI job runs `scripts/troubleshooting-lab.py`: it asserts the empty selector, repairs and checks endpoint addresses, observes an image-pull error, repairs the image to the scanned SHA, checks application health, and removes both isolated resources. Actual observations are captured in `docs/evidence/troubleshooting-ci.json` only after success.

## Actual controller integration defect and resolution

Run 39000262612 created a healthy kind cluster and a Running/Ready Traefik Pod, yet Helm timed out. Inspection of the pinned Traefik 42.0.0 chart showed the Service type moved to `service.spec.type`; the old `service.type=ClusterIP` override was ignored. Helm consequently waited for a LoadBalancer address that kind cannot provision. The fix uses `service.spec.type=ClusterIP` only in kind and `service.spec.type=LoadBalancer` in the EKS values. The controller is still health-checked; no timeout or readiness gate is bypassed. A rendered chart check now asserts the actual Service type before runtime installation.

Grafana integration follow-up: run 39001047463 deployed Traefik and metrics-server and reached a Running Prometheus, but Grafana remained 2/3 with repeated main-container restarts. The first capture did not include termination reason, so an OOM cause is not asserted. Grafana's main allowance was raised from 256 MiB to 768 MiB and container-state diagnostics were added. A pinned-chart render also revealed that `nodeExporter.enabled`, rather than the subchart's `enabled` key, controls exporter installation; the corrected lightweight preset now excludes it. Unused Alertmanager datasource provisioning is disabled with Alertmanager itself. Require actual readiness and dashboard evidence before claiming the monitoring repair succeeded.


## Verified six-step lab record

Both exercises passed in [run 39045365598](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598); [original observations](https://github.com/not-so-shubh/devops-project/blob/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence/troubleshooting-ci.json). Subsequent CI runs also preserve `troubleshooting-investigation-ci.txt` with the actual describe/EndpointSlice/Pod-label commands, image-pull events and repaired container logs before deleting the lab resources.

| Required step | Incorrect Service selector | Nonexistent image tag |
|---|---|---|
| Identify | Lab Service has zero endpoint addresses. | Lab Pod reports ErrImagePull. |
| Investigate | Describe Service; inspect EndpointSlices and actual backend Pod labels. | Describe lab Pod and kubelet events; a container that never starts has no application logs yet. |
| Root cause | Selector matches no backend Pods. | Deliberately missing registry tag cannot be pulled. |
| Fix | Patch only lab Service to backend component plus stockpilot release labels. | Set lab Deployment image to the exact scanned backend source SHA. |
| Verify | Two backend endpoint addresses are restored. | Rollout completes and in-container /health returns UP; inspect resulting container logs. |
| Document | JSON retains before=0, after=2 and verification. | JSON retains observed reason and health verification; lab resources are then removed. |

The final successful run also verifies the controller/Grafana harness corrections described above: real Traefik Ingress, authenticated Grafana and populated dashboard capture all passed. The actual dashboard preserves startup error/latency history; those observations are not erased or represented as proof of sustained production reliability.

## Frontend HIGH libx11 finding

Run 39694461786 correctly blocked promotion on CVE-2026-88806 in libx11 1.8.13-r0. Require libx11>=1.8.14-r0 from the supported Alpine repository and rerun the unchanged gate plus Compose/kind regression. See [the retained actual finding](evidence/trivy-frontend-libx11-blocked-summary.json).

## Completed AWS cleanup

The approved cleanup on 22 October removed the saved-plan resources, LB and database/worker disks and verified project residuals. [Actual record](AWS-CLEANUP-VERIFICATION.md). Do not rerun provisioning or the already-completed saved destroy plan to investigate a deleted endpoint. Private logs and backup remain in the user's CloudShell home; never publish state, plans or identifiers.
