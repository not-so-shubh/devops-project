#!/usr/bin/env bash
# Free local demonstration; uses a new named kind cluster and source-built images.
set -euo pipefail
for command in docker kind helm kubectl python3 git; do command -v "$command" >/dev/null; done
SHA=${SHA:-$(git rev-parse HEAD)}
[[ "$SHA" =~ ^[a-f0-9]{40}$ ]] || { echo 'Set SHA to a real 40-character commit'; exit 1; }
[[ "$SHA" == "$(git rev-parse HEAD)" ]] || { echo "SHA must identify the checked-out source commit"; exit 1; }
if kind get clusters | rg -qx stockpilot; then
  echo 'Cluster stockpilot already exists. Select another environment or explicitly remove the old demo first.'
  exit 1
fi
kind create cluster --name stockpilot --image kindest/node:v1.35.8@sha256:07b2536e30b803ed61d1677a79df6115f798ce64c80f9e22f6ed45afd09323c0 --wait 180s
for component in backend frontend; do
  docker build -t "ghcr.io/not-so-shubh/stockpilot-$component:$SHA" "./$component"
  kind load docker-image "ghcr.io/not-so-shubh/stockpilot-$component:$SHA" --name stockpilot
done
kubectl apply -f k8s/namespace.yaml
python3 scripts/ci-cluster-secrets.py
helm repo add traefik https://traefik.github.io/charts
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install traefik traefik/traefik --version 42.0.0 -n ingress-system --create-namespace -f monitoring/traefik-values.yaml --set service.spec.type=ClusterIP --wait --timeout 5m
helm upgrade --install metrics-server metrics-server/metrics-server --version 3.14.0 -n kube-system -f monitoring/metrics-server-kind.yaml --wait --timeout 5m
kubectl create configmap stockpilot-dashboard -n monitoring --from-file=stockpilot-dashboard.json=monitoring/stockpilot-dashboard.json --dry-run=client -o yaml | kubectl apply -f -
kubectl label configmap stockpilot-dashboard -n monitoring grafana_dashboard=1 --overwrite
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack --version 92.10.1 -n monitoring --create-namespace -f monitoring/prometheus-values.yaml --wait --timeout 10m
helm upgrade --install stockpilot helm/stockpilot -n stockpilot -f helm/stockpilot/values-prod.yaml --set backend.tag="$SHA" --set frontend.tag="$SHA" --set ingress.host=localhost --set postgres.storageClass=standard --wait --wait-for-jobs --timeout 8m
kubectl rollout status deployment/stockpilot-backend -n stockpilot --timeout=180s
kubectl rollout status deployment/stockpilot-frontend -n stockpilot --timeout=180s
kubectl exec -n stockpilot deployment/stockpilot-backend -- python -m app.seed
kubectl get pods,svc,ingress,hpa -n stockpilot
helm list -n stockpilot
cat <<'TEXT'
Run each port-forward in its own terminal:
 kubectl port-forward -n ingress-system svc/traefik 3000:80
 kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
 kubectl port-forward -n monitoring svc/monitoring-grafana 3001:80
Open http://localhost:3000 and follow docs/DEMO.md.
Grafana credentials are in monitoring/stockpilot-grafana; retrieve locally without recording the password.
This local helper builds images; CI additionally scans and publishes them. No AWS resources were created.
After collecting evidence, delete only this demo cluster: kind delete cluster --name stockpilot
TEXT
