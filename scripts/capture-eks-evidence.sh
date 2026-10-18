#!/usr/bin/env bash
# Capture real EKS evidence privately; run from an authenticated AWS CloudShell.
set -euo pipefail
umask 077
export AWS_REGION=ap-southeast-2 AWS_DEFAULT_REGION=ap-southeast-2 AWS_PAGER=""
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"
for tool in aws kubectl helm docker python3; do command -v "$tool" >/dev/null; done
docker info >/dev/null
test -s "$HOME/stockpilot-app-url.txt"
BASE_URL="$(cat "$HOME/stockpilot-app-url.txt")"
export BASE_URL
WORK_DIR="$(mktemp -d /tmp/stockpilot-browser.XXXXXX)"
EVIDENCE_DIR="$(mktemp -d "$HOME/stockpilot-eks-evidence.XXXXXX")"
ARCHIVE="$EVIDENCE_DIR.tar.gz"
PF_PIDS=()
finish() {
  result=$?
  trap - EXIT
  for pid in "${PF_PIDS[@]}"; do kill "$pid" 2>/dev/null || true; done
  mkdir -p "$EVIDENCE_DIR/browser"
  cp -R "$WORK_DIR/docs/evidence/." "$EVIDENCE_DIR/browser/" 2>/dev/null || true
  if test -d "$WORK_DIR/e2e/playwright-report"; then
    cp -R "$WORK_DIR/e2e/playwright-report" "$EVIDENCE_DIR/"
  fi
  if test -d "$WORK_DIR/e2e/test-results"; then
    cp -R "$WORK_DIR/e2e/test-results" "$EVIDENCE_DIR/"
  fi
  printf 'capture_exit_code=%s\n' "$result" > "$EVIDENCE_DIR/capture-result.txt"
  tar -czf "$ARCHIVE" -C "$EVIDENCE_DIR" .
  printf '\nPRIVATE_EVIDENCE_ARCHIVE=%s\n' "$ARCHIVE"
  printf 'This archive contains private AWS identifiers. Review it before sharing.\n'
  exit "$result"
}
mkdir -p "$WORK_DIR/e2e/tests" "$WORK_DIR/scripts" "$WORK_DIR/docs/evidence"
trap finish EXIT
cp e2e/package.json e2e/package-lock.json e2e/playwright.config.js "$WORK_DIR/e2e/"
cp e2e/tests/*.spec.js "$WORK_DIR/e2e/tests/"
cp scripts/capture-eks-browser.mjs "$WORK_DIR/scripts/"
git rev-parse HEAD > "$EVIDENCE_DIR/capture-tool-source.txt"
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$EVIDENCE_DIR/captured-at.txt"
kubectl --request-timeout=20s get nodes -o wide > "$EVIDENCE_DIR/nodes.txt"
kubectl get pods,svc,ingress,hpa,pvc -n stockpilot -o wide > "$EVIDENCE_DIR/workloads.txt"
kubectl top pods -n stockpilot > "$EVIDENCE_DIR/resource-metrics.txt"
helm list -A -o json > "$EVIDENCE_DIR/helm-releases.json"
kubectl get deployment -n stockpilot -o json > "$EVIDENCE_DIR/deployments.json"
APP_SOURCE_SHA="$(python3 - "$EVIDENCE_DIR/deployments.json" <<'PY'
import json, re, sys
items = json.load(open(sys.argv[1]))["items"]
tags = {container["image"].rsplit(":", 1)[-1]
        for item in items
        if item["metadata"]["name"] in ("stockpilot-backend", "stockpilot-frontend")
        for container in item["spec"]["template"]["spec"]["containers"]}
assert len(tags) == 1, "Backend/frontend source tags differ"
tag = tags.pop()
assert re.fullmatch(r"[0-9a-f]{40}", tag), "Expected immutable source SHA"
print(tag)
PY
)"
export APP_SOURCE_SHA
aws eks describe-cluster --name stockpilot-eks \
  --query 'cluster.{Name:name,Status:status,Version:version,Vpc:resourcesVpcConfig}' \
  --output json > "$EVIDENCE_DIR/eks-cluster.json"
aws eks describe-nodegroup --cluster-name stockpilot-eks --nodegroup-name operations \
  --query 'nodegroup.{Name:nodegroupName,Status:status,Types:instanceTypes,Scaling:scalingConfig,Health:health}' \
  --output json > "$EVIDENCE_DIR/eks-nodegroup.json"
VPC_ID="$(aws eks describe-cluster --name stockpilot-eks --query cluster.resourcesVpcConfig.vpcId --output text)"
aws ec2 describe-vpcs --vpc-ids "$VPC_ID" --output json > "$EVIDENCE_DIR/vpc.json"
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --output json > "$EVIDENCE_DIR/subnets.json"
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC_ID" --output json > "$EVIDENCE_DIR/routes.json"
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090 > "$WORK_DIR/prometheus-forward.log" 2>&1 &
PF_PIDS+=("$!")
kubectl port-forward -n monitoring svc/monitoring-grafana 3001:80 > "$WORK_DIR/grafana-forward.log" 2>&1 &
PF_PIDS+=("$!")
for port in 9090 3001; do
  for attempt in {1..30}; do
    if curl -fsS "http://127.0.0.1:$port/" >/dev/null 2>&1; then break; fi
    sleep 1
  done
  curl -fsS "http://127.0.0.1:$port/" >/dev/null
done
PLAYWRIGHT_IMAGE="mcr.microsoft.com/playwright:v1.64.1-noble@sha256:7852dc5a7d72f5fe458a597d690f6c42fbc8e9e26ddfa95f8e6ef552558d9bbf"
docker pull "$PLAYWRIGHT_IMAGE"
REQUESTS=60 bash scripts/load-test.sh
run_browser() {
  docker run --rm --init -i --network host --shm-size=512m \
  --memory=2g --cpus=1 --user "$(id -u):$(id -g)" \
  --cap-drop=ALL --security-opt=no-new-privileges \
  -e HOME=/tmp -e BASE_URL -e APP_SOURCE_SHA \
  -v "$WORK_DIR:/work" -w /work/e2e "$PLAYWRIGHT_IMAGE" "$@"
}
run_browser bash -ceu 'npm ci --ignore-scripts; npx playwright test' < /dev/null
# Credentials travel only over stdin to the monitoring capture process.
python3 - <<'PY' | run_browser node ../scripts/capture-eks-browser.mjs
import base64, json, subprocess
data = json.loads(subprocess.check_output([
    "kubectl", "get", "secret", "stockpilot-grafana",
    "-n", "monitoring", "-o", "json"
], text=True))["data"]
print(json.dumps({
    "username": base64.b64decode(data["admin-user"]).decode(),
    "password": base64.b64decode(data["admin-password"]).decode()
}))
PY
echo "PASS: real EKS browser tests and monitoring captures completed."
