# Kubernetes deliverable

Canonical bootstrap manifests are in [`k8s/`](../k8s/); the complete application manifests are in [`helm/stockpilot/templates/`](../helm/stockpilot/templates/). This directory maps the PDF's `kubernetes/` entry to the session rubric's `k8s/` and Helm layout.

The chart includes backend/frontend Deployments, ClusterIP Services, ConfigMap, externally supplied Secret references, Traefik Ingress, HPA, startup/readiness/liveness probes, migration Job and PostgreSQL StatefulSet/PVC. Secrets are created with [`scripts/create-db-secret.py`](../scripts/create-db-secret.py), not committed values. A ServiceMonitor enables Prometheus discovery when monitoring is installed.

Use the exact runbook in [DEPLOYMENT.md](../docs/DEPLOYMENT.md) for namespace/storage/controllers/secrets/monitoring before `helm upgrade --install`. For a disposable local environment, run `bash scripts/local-kind.sh` from the repository root. Real Kubernetes/Helm/Ingress/HPA/monitoring evidence is linked in [EVIDENCE.md](../docs/EVIDENCE.md); AWS EKS evidence remains separate.
