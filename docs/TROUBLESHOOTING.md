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
