# Reviewed real EKS evidence — 18 October 2026

The user supplied a real AWS CloudShell capture archive. Its exit code is **0**, and the assistant inspected the AWS/Kubernetes JSON, test receipts and six original browser images. The archive SHA-256 is `8d356ef8daae273b6869b16d2f5da3a1b149ab884269eb1a64bc0263a6ce2128`.

This is real **Sydney EKS**, not the disposable kind cluster used by CI. Capture started at **09:30:20 UTC / 15:00:20 IST**. Browser capture completed at **09:31:41 UTC**. The application images use source `84c18de84538a74a8bab92b89dc72d6e89a393d0`; the separate capture-tool checkout is `cf87b82b40151d0c21c2e03740451a1a9ed2c649`. [That tooling source's full CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39115536536) succeeded. Its [immutable CI archive](https://github.com/not-so-shubh/devops-project/tree/405b839cd453bff6086a33b1f3ce4e68c19b3384/docs/evidence) remains separately identified.

## Independent review

| Area | Inspected execution evidence | Result |
|---|---|---|
| VPC | Real VPC/subnet/route JSON | One VPC, four subnets, two availability zones |
| Public/private routing | Each subnet matched to its associated route table | Two public subnets with active IGW default routes; two private subnets with active NAT default routes; role tags correct |
| Subnet classification | MapPublicIpOnLaunch is false | Public routing is established by the IGW route; automatic public IP assignment is a separate setting |
| EKS | Real cluster and node-group JSON | Control plane ACTIVE at 1.35; managed group ACTIVE with no health issues |
| Workers | Actual Ready-node output | Two m7i-flex.large workers Ready |
| API access | Cluster network configuration | Private endpoint enabled; public operator access restricted to one /32 |
| Helm | Actual release JSON | StockPilot deployed, revision 1; Traefik, metrics-server and monitoring deployed |
| Workloads | Deployment JSON and runtime output | Two ready backend and two ready frontend replicas, one PostgreSQL Pod; completed migration |
| Database | Actual PVC output | Bound 5 GiB gp3 storage |
| Immutable images | Actual Deployment container images | Both exact source SHA tags match the application SHA above |
| Browser behavior | Existing desktop/mobile tests and report | All four scenarios passed: CRUD, editing, stock adjustment, excessive-stock rejection, retained ledger, filters/export/guide/navigation |
| Responsive page | Browser layout output and original images | Desktop width 1440 CSS pixels; mobile width 390; page scroll width matches viewport |
| Prometheus | Target API plus original Targets screenshot | Two of two application targets UP |
| Grafana | Actual browser login, datasource response and original dashboard image | Authenticated; populated request-rate, p95 latency and two-UP-target panels; numeric rate query 1.7333333333333332 requests/second |
| Security behavior | Browser received deliberate HTTP 409 responses | Insufficient-stock checks rejected as expected; browser scenarios passed |

The native Chromium launch preflight passed after installing the missing Amazon Linux libraries. The earlier Docker/vfs disk failure is preserved as a failed capture attempt in [the capture guide](AWS-EKS-CAPTURE.md); it is not counted as a successful browser run.

## Original application screenshots

These two original PNGs contain the synthetic demo application and no AWS identifiers or embedded PNG metadata. Their Git blob hashes were checked against the original attachment before publication.

![Actual EKS desktop application](evidence/eks-frontend-desktop.png)

[Actual EKS mobile viewport](evidence/eks-frontend-mobile.png)

The Prometheus image and raw AWS JSON remain private.

## Refreshed monitoring capture

The second archive was captured from the real Sydney EKS deployment at **09:57:29 UTC / 15:27:29 IST on 18 October 2026**, with browser capture at **09:59:03 UTC**. Its SHA-256 is `825d31a399760031c5054cb7076c8ef0748ba827492ad50311fefa9bbbd330eb`. Capture tooling is `13d2bf1481ef498670637914441452367d996aa3`; the running application source remains `84c18de84538a74a8bab92b89dc72d6e89a393d0`.

The archive records capture exit code zero and a passed browser-test receipt with no failed tests. Both Prometheus application targets were UP. Authenticated Grafana returned numeric live data at **2.1333333333333333 requests/second**. The live dashboard API confirms `error_ratio_axis_max=1`, and visual inspection of the original refreshed screenshot confirms **0–100%**. All four panels are populated: request rate, p95 latency, zero server-error ratio and two targets UP.

This resolves the original screenshot's autoscaled 10,000% axis. The corrected PNG remains private; its SHA-256 is `e729d2aabe61dceb620713bfdfdde053292e06ca6bb0b496b9e958835a444930`. Only identifier-free findings and file hashes are published here. The original archive provenance above is preserved separately from this follow-up.

[The capture-tool source CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39117229787) completed successfully; this does not establish an AWS Actions deployment.

## Scope and remaining steps

The full [46-row audit](RUBRIC-CHECKLIST.md) now records **42 VERIFIED criteria / 92 technical points**, **4 READY FOR DEMO points**, **2 BLOCKED cleanup points**, and **2 EXCLUDED form points**. These are evidence-coverage totals, not awarded marks.

The rubric explicitly requests AWS Console screenshots and some literal terminal captures. CLI/API provisioning is verified, while those presentation formats still require capture. A real personal security explanation and live/accepted recorded demo remain student work. OIDC listing was explicitly denied by organization policy; targeted provider lookup also returned AccessDenied. The AWS deploy job remains disabled/skipped. A green CI run and manual EKS deployment do not establish an automatic GitHub-to-EKS deployment.

Final destruction has not been evidenced in the supplied material. The original approved six-hour window ended at **17:12:07 IST on 18 October 2026** and was not reset by recovery. Current AWS resource status must be checked after reconnecting. Save remaining required evidence and a database backup, review the exact destroy scope, and obtain separate explicit final cleanup approval before teardown.

[Machine-readable capture review and file hashes](evidence/aws-eks-capture-review.json). Official form: **Student action — excluded from this task**.
