# Final submission and remaining work

Repository: https://github.com/not-so-shubh/devops-project

Verified application/infrastructure source: `9462f34dc3c8f6321af23a85d11296d980839595`. Complete successful run: https://github.com/not-so-shubh/devops-project/actions/runs/39045365598. Durable original evidence: https://github.com/not-so-shubh/devops-project/tree/48bd7092be1c403e91fc08717f75b53c61bf4295/docs/evidence. See [EVIDENCE.md](EVIDENCE.md) for screenshots and per-stage proof. Later revisions must be assessed using their own Actions run and `evidence/<source-sha>` branch.

## Work that still requires execution

| Criterion | Points | Action and required proof |
|---|---:|---|
| M3.1 | 2 | Paste the public repository URL into the instructor's official submission form. No form/link has been provided. |
| M6.3 | 1 | Explain the actual image scan and its limits yourself. Rehearse the explanation in `security/README.md`; show both current reports. |
| M7.3 | 2 | In the authorized AWS account, run a real non-empty Terraform plan and capture its output. The passing mock test is not a replacement. |
| M7.4 | 3 | Apply the reviewed plan; capture the VPC and both public subnets in the intended region. |
| M7.5 | 4 | Capture the real EKS cluster, managed node group and ready worker nodes, then deploy/verify the app there using `DEPLOYMENT.md`. |
| M7.6 | 2 | After recording the demo and collecting cloud evidence, remove demo LoadBalancers/PVCs, destroy the approved stack and capture completion plus empty state/residual-resource checks. |
| M10.2 | 3 | Present live or submit an accepted recording of your own commit -> successful pipeline -> observed deployment update. Automated kind/Flux evidence is already available; the student presentation is still required. |

The seven open criteria cover **17 of 100 points**. Other criteria have verified technical evidence; instructors award the actual marks. AWS execution needs an authenticated authorized environment, account/region confirmation and a reviewed cost/duration/cleanup scope. This session has not provisioned any AWS infrastructure.

## Required evidence formats

The reference rubric requests some screenshots in addition to command output. Preserve the complete command output too. Capture real results; the following checklist distinguishes existing screenshots from remaining capture formats.

| Requested item | Available proof / final capture |
|---|---|
| Running app/browser, desktop/mobile | Real screenshots embedded/linked in EVIDENCE.md. |
| Passing `pytest -v` terminal | Full actual 44-pass output and [browser screenshot of its original transcript](evidence/github-pytest-transcript.jpg) available. For a strict terminal-only image requirement, capture a rerun terminal during the demo. |
| At least ten descriptive commits | Existing [history screenshot](evidence/github-commit-history.jpg); [current public history](https://github.com/not-so-shubh/devops-project/commits/main/). |
| Healthy Compose terminal | [Actual healthy Compose output screenshot](evidence/github-compose-health-output.jpg) plus original logs/HTTP/persistence results available; capture the live terminal too if a literal terminal image is required. |
| Green pipeline | [Actual green summary screenshot](evidence/github-green-run.jpg) and complete run link in EVIDENCE.md. |
| GHCR package page with SHA tags | [Backend package](https://github.com/not-so-shubh/devops-project/pkgs/container/stockpilot-backend), [frontend package](https://github.com/not-so-shubh/devops-project/pkgs/container/stockpilot-frontend); [backend screenshot](evidence/github-ghcr-backend.jpg) and [frontend screenshot](evidence/github-ghcr-frontend.jpg) captured with the exact verified SHA. JSON receipts independently prove anonymous pull/source revision. |
| Trivy scan output | Both original reports and successful image-scan jobs linked in EVIDENCE.md; capture the actual job output. |
| Terraform plan / VPC / EKS / destroy | Not available; execute the real AWS lifecycle above and capture each stage. |
| Pods / Services / Helm list | [Actual Pods/Services screenshot](evidence/github-kubernetes-transcript.jpg) plus cluster/Helm transcripts available; capture Helm list and literal terminal views during the demo if required. |
| Browser through Ingress | Four actual Ingress desktop/mobile browser tests passed in the [Kubernetes job](https://github.com/not-so-shubh/devops-project/actions/runs/39045365598/job/117433652497). To show the browser address/hostname, capture the live demo after following DEPLOYMENT.md. |
| `/metrics` output | Actual exposition linked in EVIDENCE.md; capture curl/job output. |
| Prometheus Targets UP and populated Grafana | Real UI screenshots embedded in EVIDENCE.md. |
| Live demo / accepted recording | Follow DEMO.md and include your own explanation and actual deployment update. |

## Suggested presentation flow

1. Show the app, create a product, adjust inventory, demonstrate rejected overselling and retained ledger history.
2. Show PostgreSQL tests and coverage, non-root/multistage Dockerfiles, and the successful exact-SHA workflow.
3. Explain Trivy's real finding/remediation, then show both scanned/published SHA images.
4. Show running Kubernetes/Helm/Ingress/HPA, Prometheus UP targets, Grafana request/latency charts and the two diagnosis/fix/verification records.
5. Show Flux's fetched Git revision and Helm revision 2; explain why only one system owns a release.
6. Show the real AWS plan/VPC/EKS proof once executed; finish with recorded authorized cleanup evidence.

Do not submit the project as fully complete until these execution and evidence-format items are satisfied.
