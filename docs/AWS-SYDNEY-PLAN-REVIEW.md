# Sydney AWS plan and cost review

Reviewed 18 October 2026 IST. This supplements the earlier Mumbai-only readiness review. The user's AWS project is assigned to **Sydney (`ap-southeast-2`)**; Mumbai was unavailable in the displayed project console. No account upgrade or advanced-feature activation has been performed by this assistant.

## Actual execution evidence and provenance

The user ran commands in their own AWS CloudShell and supplied genuine terminal screenshots and the complete plan transcript (`Pasted text(4).txt`). The assistant reviewed those records; it did not independently run AWS commands in this account. CloudShell reported Terraform **1.14.7**, successful initialization of signed, locked AWS provider **6.69.1**, and a valid configuration. The EKS API reported Kubernetes **1.35** in `STANDARD_SUPPORT`. The user confirmed checkout `952128e01e9a`, matching source `952128e01e9afed9a0349faf7c7b58d04e5a96b5`.

[Full sanitized plan](evidence/aws-sydney-plan.txt) and [machine-readable review](evidence/aws-sydney-review.json) retain the result and provenance. The original transcript's SHA256 is recorded. Account numbers were masked by the original terminal command; this public copy additionally replaces the operator's IPv4 address with `<OPERATOR_IPV4>`. No binary plan, real tfvars, state, credentials or secrets are published.

**Actual plan: 33 to add, 0 to change, 0 to destroy.** Saved privately in CloudShell as `terraform/aws-review.tfplan`. This is real authenticated provider-backed plan evidence for **M7.3**; it is not apply, worker-node or cleanup evidence. The preceding final audit describes the earlier state and remains historical.

The plan creates one VPC (`10.42.0.0/16`), two public and two private subnets across Sydney AZs a/b, an Internet gateway, one zonal NAT/EIP, routing, three workload IAM roles and policy attachments, EKS 1.35, a managed worker group with two initial/minimum t3.large nodes (maximum four), five add-ons, EBS Pod Identity, an operator access entry and cluster-admin association, and a log group retaining seven days. The operator uses the actual stable IAM role ARN, including its `/managed/` path. Public API access is limited to the observed CloudShell egress `/32`; private API access is enabled. Recheck the egress before apply and regenerate/review the plan if it changes.

The user's later read-only output reports a **32-vCPU** standard On-Demand EC2 quota, no pending/running instances, no EKS clusters, and no IAM roles with names beginning `stockpilot-eks`. The initial two workers require **4 vCPUs**. This checks the reported quota and those name lists only; a successful plan does not prove all create/delete permissions, every service quota, resource availability or absence of every possible naming conflict.

## Current Sydney public-price estimate

Public USD rates were retrieved on 18 October 2026. The EC2/NAT/EBS offer was published 15 October 2026; the ELB offer was published 11 September 2026. Rate identifiers are preserved in the JSON review. These rates replace the earlier Mumbai estimate for this proposed deployment.

| Component | Assumption | Base USD/hour |
|---|---|---:|
| EKS standard-support control plane | 1 × $0.10/hour | 0.10000 |
| Linux t3.large workers | 2 × $0.1056/hour | 0.21120 |
| Zonal NAT gateway | 1 × $0.059/hour | 0.05900 |
| Classic ingress load balancer | 1 × $0.028/hour | 0.02800 |
| Public IPv4 | Assume 3 × $0.005/address-hour | 0.01500 |
| gp3 storage | Assume 65 GB × $0.096/GB-month / 730 hours | 0.00855 |
| **Total estimated base** | Two workers throughout | **0.42175** |

Approximate base: **$2.53 for six hours**, **$10.12 for 24 hours**, or **$307.88 for 730 hours**. The load balancer and 5 GB database PVC are later app-deployment assumptions, not additional resources already present in the 33-resource Terraform plan. The other 60 GB covers worker disks; verify actual storage types after creation. Monitoring storage is ephemeral in the existing demo configuration. Three public IP addresses is an estimate; actual LB address count can vary. No Auto Mode, provisioned control-plane tier or autoscaler-driven extra workers is included in this base.

Usage is additional: NAT data is $0.059/GB; Classic LB data is $0.008/GB. Logs, Internet/cross-AZ traffic, t3 surplus CPU credits, extra/replacement resources, taxes, exchange rates and any runtime overrun can increase costs. No free credit or account-specific discount is assumed. Public prices do not establish the user's payable bill or available credits.

Primary sources: [regional EC2/NAT/EBS offer](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.csv), [regional ELB offer](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSELB/current/ap-southeast-2/index.json), [EKS pricing](https://aws.amazon.com/eks/pricing/), [public IPv4 pricing](https://aws.amazon.com/vpc/pricing/).

## Approval boundary and remaining execution

**Approval pending. No apply, EKS worker deployment or destroy has occurred.** Proposed scope: the reviewed 33-resource plan in the user's current Building Momentum AWS project, followed by StockPilot bootstrap/deployment, one ingress load balancer and a 5 GB database PVC, for a six-hour demonstration window with a **$10 USD proposed spending target**. This target is **not an enforced hard cap**. Resources continue billing until actually deleted. Confirm the expected budget and time window before paid provisioning, as required by the user's mission instructions.

Keep state, tfvars and the saved plan privately available for later cleanup; provider downloads are in the session's temporary `TF_DATA_DIR`. The current GitHub AWS deployment job is still disabled/skipped. Before enabling it, replace its hardcoded Mumbai region with a configurable region set to Sydney, configure an appropriately scoped production OIDC role, and arrange a runner whose egress is allowed by the cluster API. Those CI changes are not claimed as executed here. OIDC permissions alone do not grant network access. Optional additional IAM/OIDC Terraform resources require a refreshed plan review within the approved scope.

After approval, recheck the saved-plan/config identity and current egress, apply the approved plan, confirm ACTIVE cluster/group and Ready workers, deploy the existing published app, and collect genuine AWS/runtime/demo evidence. Retain the evidence before requesting separate, explicit destroy/data-loss approval. Remove only approved project-owned Kubernetes load balancers/PVCs before Terraform teardown, then inspect for residual billable resources. A time estimate or an empty state alone is not proof that the whole account is cost-free.

M7.4, M7.5 and M7.6 remain unverified pending actual provisioning and cleanup. The student's personal Trivy explanation and live/accepted recording remain student presentation actions. **Official form: Student action — excluded from this task. Do not open, populate or submit it.**
