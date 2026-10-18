# AWS EKS runtime verification — 18 October 2026

Source: `84c18de84538a74a8bab92b89dc72d6e89a393d0`. [Successful source CI run](https://github.com/not-so-shubh/devops-project/actions/runs/39101728492).

This is a reviewed aggregate of commands the user actually executed in AWS CloudShell and supplied in this conversation. The assistant did not have a direct authenticated AWS session. The deployment output was supplied in `Pasted text(8).txt`; subsequent Ready-node, monitoring and IAM-policy outputs were supplied in chat. Historical kind screenshots remain evidence of kind, not AWS.

## Executed results

| Check | Observed result |
|---|---|
| Region | Sydney, ap-southeast-2 |
| EKS control plane and managed group | ACTIVE |
| Managed workers | Two m7i-flex.large nodes Ready; Kubernetes v1.35.8 |
| StockPilot Helm release | deployed, revision 1, exact source SHA above |
| Application workloads | Two ready backend replicas, two ready frontend replicas, one ready PostgreSQL replica |
| Migration | Completed |
| Database | 5 GiB gp3 PVC Bound |
| Demo seed | Eight new products |
| HTTP ingress smoke | Passed frontend-origin API access, create, stock decrement, retrieval and statistics; temporary smoke product cleaned up |
| Resource metrics | kubectl top pods succeeded |
| HPA | CPU 4% against 65% target; two replicas, configured minimum two / maximum six |
| Prometheus | Two StockPilot targets UP; measured request rate 1.423848888888889 requests/second |
| Controlled traffic | 60 successful statistics requests and 60 expected HTTP 404 responses |
| Grafana | Three of three Pod containers Ready; authenticated dashboard API access passed, all four panels configured, datasource health OK, live query 1.2952 requests/second; actual real EKS browser capture passed and was visually inspected; error-axis display fix awaits refreshed capture |

The measured CPU value verifies the HPA metric path; it is not evidence of a load-induced scale-out. Monitoring rate data came from the real EKS deployment after controlled traffic. Detailed target/query JSON is retained privately in the user's CloudShell home.

## Access recovery

A later CloudShell session had a new egress address and could not reach the allowlisted EKS API. The user executed an update restricted to the current operator /32, synchronized private Terraform variables, and then confirmed both workers Ready. Terraform state was not manually edited. A future Terraform plan must refresh remote state before any apply or destroy.

## AWS CI deployment blocker

GitHub CLI authentication and repository administrator access succeeded. The repository reports default immutable OIDC subjects. No production environment or repository Actions variables were present when checked. AWS explicitly denied listing identity providers through organization policy; a targeted lookup of the GitHub provider also returned AccessDenied. The provider's existence is therefore unconfirmed.

The AWS deployment job remains disabled/skipped. Manual Helm deployment and green CI must not be described as a successful GitHub Actions deployment to EKS. A permitted account configuration or action by the account-policy administrator is required before completing this OIDC setup.

## Remaining evidence and lifecycle

Authenticated Grafana API verification passed. Real EKS browser captures were supplied and inspected. AWS Console/terminal-format captures, student explanation/presentation and actual teardown remain outstanding. The initial six-hour approved demo window ends at 17:12:07 IST on 18 October 2026; recovery did not restart it. The US$10 amount is a spending target, not an enforced cap. Resource charges continue until deletion. Final resource destruction requires a separately reviewed scope and explicit user approval.

Official form submission: **Student action — excluded from this task.**

Machine-readable aggregate: [aws-eks-runtime-summary.json](evidence/aws-eks-runtime-summary.json).

## Inspected capture supplement

See [AWS-EKS-CAPTURE-REVIEW.md](AWS-EKS-CAPTURE-REVIEW.md) for the archive hash, per-file provenance, VPC/subnet/route inspection, four passed real EKS browser scenarios and visually inspected monitoring. The original application source remains 84c18de; capture-tool and application revisions are recorded separately.
