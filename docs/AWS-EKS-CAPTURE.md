# Capture real EKS browser evidence privately

[Documentation hub](README.md) · [Actual capture review](AWS-EKS-CAPTURE-REVIEW.md)

This is the retained operator procedure for an available, separately authorized EKS environment. The historical Sydney cluster was deleted after approved cleanup; do not run these commands expecting that old environment to exist. The CloudShell storage failure/recovery below remains a dated actual observation.

Run this after StockPilot, Prometheus and Grafana are healthy in the authorized Sydney cluster. The script uses the existing application and E2E scenarios. The default native runtime downloads only the version-matched Playwright Chromium headless shell, with browser and npm caches in /tmp. It requires Node 20 or later and the browser's system libraries. It does not provision AWS resources.

```bash
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/devops-project"
kubectl create configmap stockpilot-dashboard -n monitoring \
  --from-file=stockpilot-dashboard.json=monitoring/stockpilot-dashboard.json \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl label configmap stockpilot-dashboard -n monitoring grafana_dashboard=1 --overwrite
CAPTURE_RUNTIME=native bash scripts/capture-eks-evidence.sh
```

The capture requires AWS CLI, kubectl, Helm, Node, npm, Python and internet access in CloudShell. Install missing Amazon Linux browser libraries first:

```bash
sudo dnf install -y nss nspr atk at-spi2-atk cups-libs libdrm \
  libXcomposite libXdamage libXrandr libXfixes libXext libxcb \
  mesa-libgbm pango dejavu-sans-fonts
```

Amazon Linux is not an officially listed Playwright platform. The script runs an actual browser-launch preflight and stops if the runtime is incompatible; a downloaded browser alone is not a successful capture. An optional `CAPTURE_RUNTIME=docker` path uses the official Microsoft Playwright 1.64.1 image pinned by digest, and refuses the vfs driver because its deep copies can exhaust CloudShell disk. The operator's current /32 must be allowed by the EKS endpoint. Keep interacting with the CloudShell tab during the run to avoid idle disconnection.

The existing desktop and mobile tests create uniquely named demo products, verify editing, insufficient-stock rejection, adjustment, retained audit history, filters, export and navigation, and delete their own test products on successful completion. This is an application test workflow using synthetic data.

The script saves real VPC/subnet/route, EKS/node-group, Ready-node, workload, storage, Helm and HPA outputs, four application/dialog screenshots, a Prometheus Targets screenshot and an authenticated Grafana dashboard screenshot. Grafana credentials travel only over a pipe to the capture process and are not saved in evidence files. The native runtime executes in a temporary test-work directory. The optional Docker runtime receives only that directory rather than the repository or CloudShell home.

Successful completion prints `PASS: real EKS browser tests and monitoring captures completed.` and a `PRIVATE_EVIDENCE_ARCHIVE=` path. On a failure, a partial archive is retained with a nonzero `capture_exit_code`; it does not count as a successful capture. The script stops its own temporary port-forward processes; optional test containers use --rm.

Use CloudShell **Actions → Download file** with the exact printed archive path. Retain the originals privately. The archive includes AWS identifiers and raw target addresses; review and redact a separate publication copy before committing or uploading it publicly. Browser captures must be visually inspected before treating their presentation quality as verified.

The archive records the capture-tool checkout separately from the source SHA actually running in EKS. Fetching newer capture tooling does not deploy a new application image. Automated CI deployment remains subject to the account-policy blocker in [AWS-EKS-RUNTIME-VERIFICATION.md](AWS-EKS-RUNTIME-VERIFICATION.md).

These are automated browser tests and screenshots of the live EKS application. They are not a recording of the student's personal presentation. Final resource destruction still requires its own reviewed scope and explicit approval.

## Observed CloudShell storage failure

The first Docker capture attempt on 18 October 2026 downloaded the image but failed with `no space left on device` before browser execution. The operator retained a partial private archive. CloudShell used vfs on a 16 GiB temporary filesystem; removing only the task's cached Playwright image restored 7.7 GiB free. No EKS resources, database storage or Terraform state were removed. This failure motivated the native runtime and explicit vfs guard. The recovery is not browser success evidence.

The capture also waits for Grafana to expose the corrected error-ratio axis maximum of 1, displayed as 100%. Apply the current dashboard ConfigMap before recording a refreshed capture. The original zero-error data are preserved; this is an axis-format correction, not a metric change.
