# Deployment runbook

## Verified AWS lifecycle — 22 October 2026

The real Sydney EKS demo was provisioned, exercised and captured on 18 October. After separate explicit approval, cleanup completed at **05:16:28 IST on 22 October**: **33 Terraform resources destroyed**, two workers terminated, three EBS disks and the ingress load balancer deleted, NAT/Elastic IP/VPC/project roles/log group absent, and Terraform state empty. The database backup was downloaded and its uploaded checksum matched. [Cleanup evidence](AWS-CLEANUP-VERIFICATION.md) · [Historical EKS captures](AWS-EKS-CAPTURE-REVIEW.md).

The audit records **43 VERIFIED criteria / 94 technical points**, **4 READY FOR DEMO points** for the student's explanation/presentation, and **2 EXCLUDED form points**. These are evidence totals, not awarded marks. Supply any Console screenshots already saved and retain genuine terminal transcripts; deleted AWS Console pages cannot be recreated as authentic screenshots from CLI JSON.

[The pinned completed baseline CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39117229787) includes tests, security scans, publication and kind/Flux validation. Later sources have their own [Actions results](https://github.com/not-so-shubh/devops-project/actions/workflows/ci-cd.yml) and `evidence/<source-sha>` reports. A subsequent libx11 security failure and package remediation are recorded in [the security explanation](TRIVY-EXPLANATION.md); publication remains gated by HIGH/CRITICAL scans.

Automatic EKS deployment remains disabled because account policy blocked OIDC-provider access. Use a permitted local/CI environment for a new personal demonstration and label it accurately; a new paid AWS environment requires a new reviewed cost/runtime approval. Official form: **Student action — excluded from this task**.
Bootstrap examples below are reusable procedures for a separately authorized environment. On an existing installation, preserve its database Secret on retries. The database retains its original password on the PVC. Re-running a disposable-kind secret generator on EKS could rotate only the Secret and break database authentication.

See [AWS-READINESS.md](AWS-READINESS.md) for the current preparation, evidence boundaries and remaining actions. Official form submission: **Student action — excluded from this task.**

## Local stack and image design

From repository root, copy `.env.example` to `.env`, set a long URL-safe password, then `docker compose config --quiet` and `docker compose up --build -d --wait --wait-timeout 180`. Open localhost:3000. The one-shot `migrate` service must finish before backend starts; frontend starts after database-aware backend health passes. `docker compose exec backend python -m app.seed` is explicit and repeatable.

Backend uses digest-pinned Python 3.12 Alpine and installs hash-locked binary runtime dependencies only, removes installer tooling, runs as 10001, and exposes 8000. Frontend builds with locked Node dependencies, copies static assets into unprivileged Nginx, runs as 101 on 8080, and uses SPA fallback plus the unchanged `/api` prefix. Both runtime filesystems are read-only with temporary storage, dropped capabilities, health checks and no privilege escalation. Frontend manifests remain outside the web root, but the image scanner inventories only its root Node package; a separate blocking npm lockfile audit covers the dependency graph including build dependencies. Base images are digest-pinned; refresh them intentionally and rerun scans to pick up security fixes.

## CI/CD and GHCR

Push a real code change to `main`. Quality and infrastructure jobs run first. Compose runs HTTP and desktop/mobile acceptance against PostgreSQL. Separate images are then built and scanned; HIGH/CRITICAL findings, including unfixed findings, block promotion. The publish matrix loads the saved scanned image and pushes the source SHA tag. Pull requests get validation without publishing or AWS access.

```bash
SHA=$(git rev-parse HEAD)
docker pull "ghcr.io/not-so-shubh/stockpilot-backend:$SHA"
docker pull "ghcr.io/not-so-shubh/stockpilot-frontend:$SHA"
```

The initial GHCR packages may be private. In GitHub package settings, either make both public for the public demonstration or create a durable Kubernetes `imagePullSecret` from a least-privilege read:packages token. Do not use the short-lived job GITHUB_TOKEN for future cluster pulls. Confirm access from the actual cluster before calling the deployment successful. Run `python3 scripts/create-registry-secret.py` to create `ghcr-pull` interactively without exposing a token in command arguments. Supply `--set 'imagePullSecrets[0].name=ghcr-pull'` for manual Helm, and set GitHub variable `GHCR_PULL_SECRET=ghcr-pull` for the deployment job if packages remain private. For Flux, add `imagePullSecrets: [{name: ghcr-pull}]` under release values. Never put a token in Git or Helm values.

## Disposable Kubernetes verification

The workflow provisions a free kind cluster on its ephemeral runner, loads the exact scanned image tarballs, installs Traefik, metrics-server and kube-prometheus-stack, runs Helm, and tests through actual Ingress. This gives genuine portable Kubernetes evidence without creating paid infrastructure. It does not satisfy the rubric's separate requirement for an AWS VPC/EKS apply/destroy demonstration.

To reproduce a free local demonstration with Docker, kind, Helm, kubectl, Git and Python installed, run `bash scripts/local-kind.sh` from the repository root (allocate at least 8 GB RAM). It creates only a new digest-pinned Kubernetes 1.35.8 kind cluster matching the EKS 1.35 minor, builds source images, installs the pinned controllers and monitoring, and prints the port-forwards. It refuses to overwrite an existing `stockpilot` cluster. Source-built images avoid GHCR pull permissions; this helper does not replace CI security scanning. Stop Compose with `docker compose down` before forwarding kind Ingress to the same local port 3000 (the Compose volume is retained). These are separate demo databases. Collect evidence before `kind delete cluster --name stockpilot`.

## AWS preparation — approval required before apply

Use an AWS CLI SSO/profile with the authorized account. Confirm `aws sts get-caller-identity`; do not copy credentials into this repository. Review current regional prices and the intended duration before obtaining explicit cost approval. The plan uses two t3.large workers, a control plane, NAT/EIP, EBS, logging, and an Ingress load balancer. This runbook does not constitute approval.

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit account-specific IAM role ARN and trusted API CIDRs.
terraform fmt -check -recursive
terraform init -lockfile=readonly
terraform validate
terraform test
terraform plan -out=stockpilot.tfplan
# STOP for review of costs, account, resource plan and cleanup scope.
# Only after explicit approval:
terraform apply stockpilot.tfplan
terraform output
aws eks update-kubeconfig --region ap-south-1 --name stockpilot-eks
kubectl get nodes
cd ..
```

The default loopback CIDR prevents accidental broad public API access; replace it with the operator's /32 or runner egress ranges. A private/self-hosted runner inside the VPC is preferable for CI access. For a hosted runner, its current egress must be allowed deliberately; OIDC alone does not provide network connectivity. Bootstrap resources below as an operator, not the namespace-limited CI role.

## Bootstrap EKS storage, ingress, metrics and secrets

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/storage-class.yaml
kubectl get csidriver ebs.csi.aws.com
helm repo add traefik https://traefik.github.io/charts
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install traefik traefik/traefik --version 42.0.0 \
  -n ingress-system --create-namespace -f monitoring/traefik-values.yaml --wait --timeout 5m
helm upgrade --install metrics-server metrics-server/metrics-server --version 3.14.0 \
  -n kube-system --wait --timeout 5m
python3 scripts/create-db-secret.py
```

The database helper reads a password without echo, URL-encodes it, and applies `stockpilot-db` via stdin without writing a secret file. Keys are `username`, `password`, and `database-url`; the chart only references the existing Secret. Keep the database name `stockpilot` consistent. For external PostgreSQL, disable `postgres.enabled`, supply a verified TLS URL and trust store, and arrange backups/restore independently. The kind-only insecure kubelet-TLS values file must not be used on EKS.

Create Grafana credentials interactively, without a password on the shell command line:

```bash
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
python3 scripts/create-grafana-secret.py
kubectl create configmap stockpilot-dashboard -n monitoring \
  --from-file=stockpilot-dashboard.json=monitoring/stockpilot-dashboard.json \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl label configmap stockpilot-dashboard -n monitoring grafana_dashboard=1 --overwrite
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack --version 92.10.1 \
  -n monitoring -f monitoring/prometheus-values.yaml --wait --timeout 10m
```

## Deploy and prove the Helm release

Use the exact published 40-character SHA from the successful run, not an invented tag:

```bash
SHA=$(git rev-parse HEAD)
helm lint helm/stockpilot --set backend.tag="$SHA" --set frontend.tag="$SHA"
helm template stockpilot helm/stockpilot -n stockpilot -f helm/stockpilot/values-prod.yaml \
  --set backend.tag="$SHA" --set frontend.tag="$SHA" > /tmp/stockpilot-rendered.yaml
kubectl apply --dry-run=client -f k8s/namespace.yaml
helm upgrade --install stockpilot helm/stockpilot -n stockpilot \
  -f helm/stockpilot/values-prod.yaml --set backend.tag="$SHA" --set frontend.tag="$SHA" \
  --set ingress.host=stockpilot.local --wait --wait-for-jobs --timeout 10m
kubectl rollout status deployment/stockpilot-backend -n stockpilot --timeout=180s
kubectl rollout status deployment/stockpilot-frontend -n stockpilot --timeout=180s
kubectl get pods,svc,ingress,hpa -n stockpilot
helm list -n stockpilot
kubectl top pods -n stockpilot
kubectl exec -n stockpilot deployment/stockpilot-backend -- python -m app.seed
```

One chart release per namespace is supported. The migration Job is an ordinary Job named by release revision, avoiding pre-install database ordering and post-install readiness deadlocks. `--wait-for-jobs` checks completion, while backend readiness prevents early API traffic. Do not run simultaneous Helm upgrades. A rollback restores images/values, not database state.

Get the load balancer address with `kubectl get svc traefik -n ingress-system`. For a DNS name, set a CNAME for your own hostname and override `ingress.host` accordingly. For the demo without DNS:

```bash
LB=$(kubectl get svc traefik -n ingress-system -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl --fail -H 'Host: stockpilot.local' "http://$LB/api/inventory/stats"
```

For a browser, use your hostname/DNS or port-forward the controller and set a local hosts entry for `stockpilot.local`. `kubectl port-forward -n ingress-system svc/traefik 3000:80` then open `http://stockpilot.local:3000`. A hosts entry maps a name to an IP, never to an AWS load-balancer DNS name. TLS requires your own certificate Secret and `ingress.tls` values; do not claim the HTTP capstone endpoint is TLS-secured.

## HPA and observability evidence

```bash
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl top pods -n stockpilot
kubectl get hpa -n stockpilot -w
# In another terminal, use your real reachable ingress URL:
BASE_URL=http://stockpilot.local:3000 REQUESTS=500 bash scripts/load-test.sh
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
kubectl port-forward -n monitoring svc/monitoring-grafana 3001:80
```

Port-forward processes require separate terminals. Prometheus: localhost:9090/targets; require StockPilot target UP. Grafana: localhost:3001, log in with your externally supplied credentials, open **StockPilot · Operations**. Generate sustained traffic and wait at least two scrape intervals. Request rate, p95 latency, 5xx ratio and target count panels use actual metric names. `python3 scripts/verify-monitoring.py` asserts UP plus a positive request-rate query through the Prometheus port-forward. A zero 5xx rate is legitimate; an empty request graph is not evidence of monitoring.

HPA may correctly stay at two replicas under low CPU. Prove its metrics are available; do not claim scale-out unless observed. Do not expose Prometheus or Grafana publicly without authentication/TLS. See docs/EVIDENCE.md for capture requirements.

## Enable continuous EKS deployment

Only after manual bootstrap and successful cluster pulls:

1. Create/reuse GitHub's account OIDC provider; supply its ARN to Terraform and review/apply the resulting role/access changes under the same AWS cost/account authorization.
2. Protect the repository's `production` environment and restrict deployment to `main`.
3. Set GitHub variables `AWS_ROLE_ARN`, `EKS_CLUSTER_NAME`, `INGRESS_HOST`, and `AWS_REGION` to match the Terraform deployment. The approved CloudShell project uses Sydney (`AWS_REGION=ap-southeast-2`); an unset variable retains the Mumbai default. Both AWS authentication and kubeconfig use this same region. If appropriate, set `DEPLOY_RUNNER` for a connected private runner.
4. Confirm the role has an EKS access entry and namespace EditPolicy, the EKS API allowlist admits the runner, and `stockpilot-db`, gp3 storage, ingress/metrics/monitoring already exist.
5. Set `AWS_DEPLOY_ENABLED=true`. Push a real change and verify the exact new image SHA and rollout.

For this repository, the public GitHub API reports owner ID `180390682`, repository ID `1422512974`, and creation on 16 October 2026. GitHub's [immutable OIDC subject format](https://github.blog/changelog/2026-04-23-immutable-subject-claims-for-github-actions-oidc-tokens/) applies to repositories created after 15 July 2026. Before enabling the optional Terraform deployment role, set `github_repository = "not-so-shubh@180390682/devops-project@1422512974"` in the private tfvars. The existing trust template then produces the exact production subject `repo:not-so-shubh@180390682/devops-project@1422512974:environment:production`. Verify the repository's actual OIDC settings before applying the IAM plan; keep the trust scoped to this exact repository/environment and `sts.amazonaws.com`. Leave the optional provider disabled until this separate role/access plan has been reviewed. The current 33-resource network/cluster plan does not create this GitHub role.

The pipeline intentionally cannot bootstrap cluster-wide infrastructure with its deployment role. A failed deployment is visible and fails the job. No paid infrastructure is created by the workflow.

## Cleanup after evidence and authorization

Collect VPC, EKS, node, Helm, ingress, monitoring and demo evidence before cleanup. Inspect the exact namespace/account before deleting anything.

```bash
helm uninstall stockpilot -n stockpilot
# Explicit deletion of demonstration data; retain/backup business data instead.
kubectl delete pvc -n stockpilot -l app.kubernetes.io/name=stockpilot
# If the PVC has no matching label, inspect and delete the exact demo claim:
kubectl get pvc -n stockpilot
# kubectl delete pvc data-stockpilot-postgres-0 -n stockpilot
helm uninstall traefik -n ingress-system
helm uninstall monitoring -n monitoring
kubectl get svc -A                    # verify demo LoadBalancer removal
cd terraform
terraform plan -destroy
# After cleanup approval in the intended account:
terraform destroy
terraform state list
```

StatefulSet PVCs deliberately survive ordinary Helm uninstall. The exact claim is `data-stockpilot-postgres-0`; delete it explicitly only when demo-data destruction is authorized. Wait for load-balancer and EBS cleanup before deleting the VPC/node infrastructure. Capture the real destroy completion and check AWS for remaining billable resources. Never invent cleanup evidence.
