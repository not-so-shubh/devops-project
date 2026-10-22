# Terraform and the AWS lifecycle

[Documentation hub](../docs/README.md) · [AWS readiness](../docs/AWS-READINESS.md) · [Verified cleanup](../docs/AWS-CLEANUP-VERIFICATION.md)

The real Sydney capstone infrastructure was provisioned, manually deployed, captured and **deleted after separate approval on 22 October 2026**. This directory contains reusable code, not a currently running AWS environment.

## Defined resources

Two-AZ VPC with two public/two private subnets, IGW, one NAT/EIP and routes; EKS API and managed workers; project IAM/access entries; network/Pod Identity add-ons; EBS CSI with a dedicated role; and a seven-day cluster log group. The optional GitHub deployment role is disabled unless an existing permitted OIDC provider ARN is supplied.

Terraform requires `>=1.14,<2`; CI uses 1.14.7 and locks AWS provider 6.69.1. Templates default to `ap-south-1` and `t3.large`. The executed account used **Sydney `ap-southeast-2` and `m7i-flex.large`** after an approved worker repair. Region/type defaults do not establish current account eligibility or cost.

## Validation without provisioning

From this directory:

```bash
terraform fmt -check -recursive
terraform init -input=false -lockfile=readonly
terraform validate
terraform test
```

Tests use a mock provider and create no AWS infrastructure. These commands are not evidence of a provider-backed account plan. The historical real plan showed 33 additions; [actual plan and runtime provenance](../docs/EVIDENCE.md#historical-aws-lifecycle).

## Future authorized account plan

Use [`terraform.tfvars.example`](terraform.tfvars.example) as a template for private variables. Select explicit region/types, a stable IAM user/role ARN rather than an STS session ARN, and restricted trusted API CIDRs. The public endpoint default is loopback; do not replace it with unrestricted access. A private endpoint is enabled too.

Confirm identity, regional availability/quotas, current pricing, duration and backup/cleanup scope before generating and reviewing a real saved plan. The historical approval is not approval for a new environment. State, saved plans, actual tfvars, keys and kubeconfig remain outside Git. Shared operations need protected remote state/locking; retain secure state backups for teardown.

## OIDC and network access

The assigned account denied OIDC-provider listing and targeted provider lookup; the optional AWS deployment job stayed disabled. Provider existence is unconfirmed. A permitted future setup must use the repository's actual OIDC subject claims, audience `sts.amazonaws.com`, protected production environment and namespace-scoped EKS access. Query current subject settings rather than assuming the repository-name-only format. IAM authentication does not provide a runner route through the EKS API allowlist.

## Actual cleanup boundary

The operator separately approved **33 Terraform deletions**, one Kubernetes-created LB and the database volume. LB/PVC deletion was confirmed while controllers still existed, then the saved destruction plan was applied. The exact command was `terraform apply <saved-destroy-plan>` following `terraform plan -destroy -out=...`; do not claim a different literal command was typed. Empty state, terminated workers, three absent EBS disks and scoped AWS residual checks passed. [Full result](../docs/AWS-CLEANUP-VERIFICATION.md).

The original six-hour window was exceeded; actual charges/credits are unverified. One NAT and single database are documented capstone tradeoffs, not production HA. No cloud action is needed for this documentation/media handoff.
