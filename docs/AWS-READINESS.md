# AWS readiness, cost estimate and remaining execution

## Subsequent executed AWS session

The earlier preflight below is historical. The user later used AWS CloudShell in the assigned **Sydney (ap-southeast-2)** managed account, approved the reviewed plan/cost/runtime, provisioned the VPC and EKS, repaired the failed empty worker group with two m7i-flex.large workers, deployed StockPilot and supplied the inspected real EKS evidence. See [capture review](AWS-EKS-CAPTURE-REVIEW.md) and [runtime verification](AWS-EKS-RUNTIME-VERIFICATION.md).

The approved six-hour window started 11:12:07 IST and ends 17:12:07 IST on 18 October 2026; the US$10 amount is a spending target, not a hard cutoff. No account upgrade has been performed. Final cleanup is not yet authorized or executed. OIDC listing was explicitly denied by organization policy and direct provider lookup also returned AccessDenied; the AWS Actions deployment job remains disabled. The earlier Mumbai assumptions and no-access statement below must not be used as current session status.

## Historical preflight


Reviewed 18 October 2026 IST against source `710d1460abc480d8b19e2b98f648a9a5c1c23339`. Intended region: **Mumbai, ap-south-1**. No AWS account identity has been established in this workspace. No real plan, apply, EKS deployment or destroy has occurred. The existing `terraform-plan.txt` is an earlier failed attempt, not successful AWS evidence.

## Executed readiness checks

The workspace has no AWS CLI, AWS environment configuration or suitable EKS provisioning connector. No credential values were read or printed. STS identity, IAM/service permissions and quotas therefore remain unverified. [cloud-access-check.json](evidence/cloud-access-check.json) records the actual boundary.

Official Terraform 1.14.7 was downloaded from HashiCorp and its SHA256 checked against the official release checksums. `fmt -check -recursive` passed. Locked `init` initially failed because the temporary directory was unavailable; retrying with `TMPDIR` set to the repository's ignored `.tmp` succeeded and installed the signed AWS provider 6.69.1. Local `validate` and `test` then failed before loading provider schemas: the provider did not complete startup in this restricted workspace, which also lacks `/proc/self/exe`. These are preserved as failures in [terraform-local-readiness.txt](evidence/terraform-local-readiness.txt), not represented as successful local validation.

The reviewed [main infrastructure job](https://github.com/not-so-shubh/devops-project/actions/runs/39070661297/job/117507399134) successfully initialized the actual locked provider, validated the configuration and ran the mocked topology test in GitHub's runner. The new publishing commit runs those checks again. A passing mock test still does not satisfy M7.3–M7.6.

## Terraform architecture review

| Area | Reviewed implementation and remaining preflight |
|---|---|
| Versions/providers | Terraform >=1.14,<2; `hashicorp/aws ~>6.69.0`, lock selects 6.69.1. No external Terraform modules. Keep the lockfile and use `init -lockfile=readonly`. |
| Kubernetes support | [AWS release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html) lists EKS 1.35 in standard support through 27 March 2027. Before apply, confirm **regional/account** availability with `aws eks describe-cluster-versions --region ap-south-1 --cluster-versions 1.35` and inspect status/add-on compatibility. No account-level check has run here. |
| Network | DNS-enabled 10.42.0.0/16 VPC; two public 10.42.101/102.0/24 and two private 10.42.1/2.0/24 subnets in the first two available AZs. Verify account AZs and CIDR conflicts. Public routes use IGW; private default route uses the single NAT/EIP. |
| Discovery/naming | Public/private ELB role tags are present. Provider default tags identify StockPilot/environment/Terraform; cluster-derived IAM/resource names must not conflict with existing resources. |
| Workers | Two desired/minimum, maximum four, on-demand t3.large AL2023 x86 workers on private subnets; 30 GiB root disk each. Verify instance availability, EC2/vCPU quotas and workload capacity. These are EKS managed node groups, not EKS Auto Mode. |
| API/security groups | Private API enabled; public API restricted to `admin_cidrs`, loopback by default. Replace with trusted operator/runner CIDRs; no 0.0.0.0/0. EKS manages the cluster security group used by managed workers; verify actual rules/connectivity after creation. |
| Operator IAM | Cluster creator bootstrap-admin disabled; explicit API access entry. For assumed roles, set the stable IAM role ARN in `admin_principal_arn`, never an STS session ARN or account-root ARN. Review provisioning permissions including scoped PassRole and service-linked roles with the account administrator. |
| Worker/storage IAM | Worker, registry pull and CNI policies on the node role; EBS CSI gets a separate Pod Identity role/policy. Pod Identity agent and EBS driver are declared. Moving CNI permissions off nodes is further hardening, not a claim already implemented. |
| Add-ons | VPC CNI, CoreDNS, kube-proxy, Pod Identity agent and EBS CSI. Select/verify compatible add-on versions with the real regional API before creation; do not treat mocked data as availability proof. |
| OIDC | Optional existing GitHub OIDC provider; trust requires this repo's `production` environment and STS audience. App role only describes this cluster and edits the `stockpilot` namespace; operator bootstraps storage/controllers/secrets. Runner network access is separately required. |
| State/outputs | VPC/subnet/cluster/node outputs exist. State/plans/real tfvars are ignored. Retain encrypted, access-controlled state and backups outside public Git; use locked remote state for shared work. Do not lose state needed for cleanup. |
| Destroy | Explicit resource dependencies and Terraform-managed log group support teardown. Kubernetes-created LBs/PVs must be removed and verified first. PVC retention is intentional; AWS service-linked roles/account OIDC providers are not automatically project-owned. |

No broad infrastructure rewrite is needed from this code review. Actual permission, availability, quota, controller and destroy compatibility remain account-dependent checks, not verified deployment claims.

## Current public regional pricing and proposed runtime

Public AWS price data was retrieved on 17 October 2026 UTC (18 October IST); [aws-public-pricing.json](evidence/aws-public-pricing.json) retains source URLs, product/rate identifiers, publication dates and assumptions. These are public on-demand USD rates, not an account-specific quote. EC2/NAT/gp3 source publication: 15 October 2026; Classic ELB source publication: 11 September 2026.

| Component | Quantity / rate | Approximate hourly base |
|---|---|---:|
| EKS standard control plane | 1 × $0.10/cluster-hour | $0.10000 |
| Linux t3.large workers | 2 × $0.0896/instance-hour | $0.17920 |
| Zonal NAT gateway | 1 × $0.056/hour; $0.056/GB processed separately | $0.05600 |
| Classic Load Balancer, existing controller design | 1 × $0.0266/hour; $0.008/GB separately | $0.02660 |
| Public IPv4 | Assume NAT plus two LB addresses: 3 × $0.005/address-hour; actual LB address count may differ | $0.01500 |
| gp3 volumes | 60 GiB worker disks + 5 GiB PostgreSQL, $0.0912/GB-month, 730-hour estimate | $0.00812 |
| **Estimated base** | Excludes usage charges below | **$0.38492/hour** |

Six hours of base runtime is approximately **$2.31**; 24 hours approximately **$9.24**. Proposed approval envelope: **up to $10 USD for six hours**, including provisioning/demo/cleanup time and allowance for small data transfers/logging. This is a proposal, **not approved and not an enforced hard cap**. Taxes, exchange rates, credits, CloudWatch log ingestion/storage, Internet and cross-AZ data, NAT/LB traffic, t3 surplus CPU credits, extra/replacement nodes/LBs/IPs and overruns change the total. The same base left running for 730 hours is about $281 before those extras. Confirm rates and actual resources again before approval.

Prometheus/Grafana use ephemeral storage in the capstone values; no separate monitoring EBS volume is assumed. If the ingress controller is changed to NLB/ALB or EKS Auto Mode, recalculate its pricing and IAM requirements. The current plan assumes the documented legacy Classic LB path; no LB exists here. No free-tier credit is assumed.

Primary sources: [EKS pricing](https://aws.amazon.com/eks/pricing/), [regional EC2/NAT/EBS offer](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-south-1/index.csv), [regional ELB offer](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSELB/current/ap-south-1/index.json), [IPv4 pricing](https://aws.amazon.com/vpc/pricing/).

## Minimum secure connection and approval sequence

1. Use an authorized AWS account and an ephemeral SSO/profile session in an execution environment with AWS CLI, Terraform, kubectl, Helm and Docker/browser access. Use your normal secure AWS authentication mechanism; do not paste keys, passwords or session tokens into chat, Git or screenshots. This session has no mechanism to receive a supported AWS session yet.
2. Run `aws sts get-caller-identity --profile <authorized-profile>` privately, select `AWS_PROFILE` and `AWS_REGION=ap-south-1`, and confirm the intended account and stable operator role. Share only a suitably masked identity if evidence is public.
3. With the account administrator verify least-privilege VPC/EC2/EKS/IAM/CloudWatch provisioning and deletion permissions, scoped `iam:PassRole`, required service-linked roles, EC2/vCPU/EIP/EKS quotas, CIDR/name conflicts and two available AZs. Read-only calls and a successful plan do not prove all create/delete permissions.
4. Check EKS 1.35 and compatible add-ons through the regional API, then configure trusted API CIDRs and the stable IAM principal in ignored tfvars. Review local-state handling or an existing approved encrypted locked backend.
5. Run actual fmt/init/validate/test and a **real, nonempty provider-backed plan** with the authenticated account. Save private plan/state securely; export only reviewed sanitized text. Check region, topology, IAM, resource counts and all replacements/deletions.
6. Review that exact plan plus current prices and get explicit approval of account, resource scope, **$10/six-hour proposed envelope or an agreed alternative**, CI deployment scope and capture schedule. **Do not apply or enable AWS deployment before approval.** No approval is implied by these instructions.
7. Apply the approved saved plan and follow [DEPLOYMENT.md](DEPLOYMENT.md): bootstrap EBS/controller/metrics/monitoring/secrets, deploy the published SHA, verify API/browser/persistence/replicas/HPA, capture EKS-only screenshots and save command output. Confirm Ready nodes, ACTIVE managed group and actual region/resource identities.
8. Configure GitHub production environment/OIDC/runner variables only within the approved scope. Keep Flux suspended if Actions owns the release. Trigger the meaningful commit and verify the deploy job **succeeds**, live images equal its source SHA, Helm revision changes and UI updates. A skipped AWS job is not EKS evidence.
9. Capture app, VPC, EKS, nodes, Helm, Ingress, monitoring and the student recording; verify saved evidence is readable. If the presentation needs a live cluster later, review the ongoing cost/recreation tradeoff.
10. Separately review the exact disposable teardown scope and obtain explicit destroy/data-loss approval. Remove demo LBs/PVCs and await deletion, run the reviewed destroy, verify empty project state and inspect region/account for residual LBs, EBS/snapshots, EIPs, ENIs, NATs and logs. Do not delete unrelated resources or claim the entire account is cost-free from an empty Terraform state alone.

Update M7.3–M7.6 only after the respective real commands and AWS resource/cleanup verification. Screenshot requirements remain real terminal/console captures, never simulated output. Official form submission is **Student action — excluded from this task.**
