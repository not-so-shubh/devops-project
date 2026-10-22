# Kubernetes and Helm

[Documentation hub](../docs/README.md) · [Deployment](../docs/DEPLOYMENT.md) · [Monitoring](../monitoring/README.md)

This coursework directory points to canonical [`k8s/`](../k8s/) bootstrap manifests and [`helm/stockpilot/`](../helm/stockpilot/) chart files.

| Object | Role |
|---|---|
| Backend/frontend Deployments | At least two replicas in production values, probes and non-root containers |
| ClusterIP Services | Named HTTP ports, backend 8000 and frontend 8080 |
| Traefik Ingress | `/api` to backend and `/` to frontend |
| Migration Job | Ordinary release-revisioned Alembic step; backend readiness checks schema |
| PostgreSQL StatefulSet/PVC | Single database replica; `standard` on kind or `gp3` on EKS |
| ConfigMap/Secret references | Non-secret runtime configuration and externally supplied credentials |
| HPA | Backend minimum 2, maximum 6, CPU target 65% |
| ServiceMonitor | Prometheus backend discovery through the named `http` Service port |

Use `bash scripts/local-kind.sh` from the repository root for a new disposable local environment. It refuses to overwrite an existing named cluster. The full command sequence, prerequisites and verification live in [Deployment](../docs/DEPLOYMENT.md#local-kind).

Create Secrets only for a fresh installation using [`create-db-secret.py`](../scripts/create-db-secret.py) and [`create-grafana-secret.py`](../scripts/create-grafana-secret.py), or retain the credentials matching existing data. Do not rotate a Kubernetes Secret independently of an initialized database. Never use the disposable CI secret generator on an existing EKS database.

The [kind integration proof](https://github.com/not-so-shubh/devops-project/blob/fa40366375c8a05edbe6a0837071e988d496e62b/docs/evidence/kubernetes-ci.txt) and [historical real EKS proof](../docs/AWS-EKS-CAPTURE-REVIEW.md) are distinct. Real EKS was manually deployed and later destroyed after approval; no AWS cluster remains from that demonstration. [Cleanup](../docs/AWS-CLEANUP-VERIFICATION.md).
