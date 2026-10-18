# Capture real EKS browser evidence privately

Run this after StockPilot, Prometheus and Grafana are healthy in the authorized Sydney cluster. The script uses the existing application, its existing E2E scenarios, and an official Playwright 1.64.1 container pinned by digest. Package and browser versions match. It does not provision AWS resources.

```bash
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/devops-project"
bash scripts/capture-eks-evidence.sh
```

The capture requires AWS CLI, kubectl, Helm, Docker, Python and internet access in CloudShell. The operator's current /32 must be allowed by the EKS endpoint. Keep interacting with the CloudShell tab during the run to avoid idle disconnection.

The existing desktop and mobile tests create uniquely named demo products, verify editing, insufficient-stock rejection, adjustment, retained audit history, filters, export and navigation, and delete their own test products on successful completion. This is an application test workflow using synthetic data.

The script saves real VPC/subnet/route, EKS/node-group, Ready-node, workload, storage, Helm and HPA outputs, four application/dialog screenshots, a Prometheus Targets screenshot and an authenticated Grafana dashboard screenshot. Grafana credentials travel only over a pipe to the capture process and are not saved in evidence files. The container receives a temporary test-work directory rather than the repository or CloudShell home.

Successful completion prints `PASS: real EKS browser tests and monitoring captures completed.` and a `PRIVATE_EVIDENCE_ARCHIVE=` path. On a failure, a partial archive is retained with a nonzero `capture_exit_code`; it does not count as a successful capture. The script stops only its own temporary port-forward processes and test container.

Use CloudShell **Actions → Download file** with the exact printed archive path. Retain the originals privately. The archive includes AWS identifiers and raw target addresses; review and redact a separate publication copy before committing or uploading it publicly. Browser captures must be visually inspected before treating their presentation quality as verified.

The archive records the capture-tool checkout separately from the source SHA actually running in EKS. Fetching newer capture tooling does not deploy a new application image. Automated CI deployment remains subject to the account-policy blocker in [AWS-EKS-RUNTIME-VERIFICATION.md](AWS-EKS-RUNTIME-VERIFICATION.md).

These are automated browser tests and screenshots of the live EKS application. They are not a recording of the student's personal presentation. Final resource destruction still requires its own reviewed scope and explicit approval.
