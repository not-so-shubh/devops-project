# AWS status and operator readiness

[Documentation hub](README.md) · [Terraform](../terraform/README.md) · [Runtime proof](AWS-EKS-RUNTIME-VERIFICATION.md) · [Cleanup](AWS-CLEANUP-VERIFICATION.md)

## Completed historical lifecycle

The assigned account's actual execution used **Sydney (`ap-southeast-2`)**, not the earlier proposed Mumbai default. The user approved the provider-backed 33-resource plan, provisioned the VPC/EKS, repaired an empty failed worker group under reviewed scope, deployed StockPilot manually and supplied real application/monitoring captures.

On **22 October 2026**, after a separate explicit cleanup approval and downloaded database backup, the operator removed the ingress LB/PVC assets, applied the saved destruction plan and passed scoped residual checks. Terraform state is empty and the reviewed environment is deleted. [Exact cleanup provenance](AWS-CLEANUP-VERIFICATION.md).

The original six-hour window ended on 18 October and was exceeded. The US$10 amount was a spending target, not an automatic cutoff. Actual charges, credits and taxes are unverified.

## Account-policy blocker

GitHub CLI login/repository administrator access succeeded. AWS organization policy explicitly denied OIDC-provider listing; a targeted provider lookup also returned AccessDenied. The provider's existence is unconfirmed. No account upgrade, permanent AWS-key workaround or successful automatic EKS Actions deployment is claimed. The optional job remains disabled.

Authentication, EKS authorization and API network reachability are separate requirements. CloudShell egress changes were repaired by updating only the trusted operator `/32` and synchronizing private variables. State was not manually edited. [Operator helper](../scripts/refresh-eks-access.sh).

## Future permitted deployment checklist

This is preparation only, not authorization to recreate paid infrastructure:

1. Establish the intended AWS account/profile and permitted region without sharing credentials.
2. Verify current EKS/type availability, quotas, IAM permissions and any free-plan restrictions.
3. Choose explicit region/types/CIDRs. Templates default to Mumbai and `t3.large`; the historical account used Sydney and `m7i-flex.large`.
4. Review current regional costs, expected duration, data-loss/backup needs and a concrete real plan before cost approval.
5. Preserve private state/plans/variables and use protected remote state/locking for shared operations.
6. Bootstrap storage/controllers/Secrets and test actual registry/API access before app deployment.
7. Save evidence and personal recording before separately approved LB/PVC/infrastructure cleanup.

Use the [deployment guide](DEPLOYMENT.md) and [Terraform README](../terraform/README.md) for responsibilities. A mock-provider test is not a real account plan. None of these cloud actions are part of the current documentation/media polish.

## Preserved initial preflight

The [immutable 18 October preflight narrative and historical cost assumptions](https://github.com/not-so-shubh/devops-project/blob/8944da7ddf2be0845a593c2f65482eb922e6d9f7/docs/AWS-READINESS.md) retains the original Mumbai proposal, restricted-workspace provider failures and dated price references. It preceded the actual Sydney deployment and does not describe current resources or current prices. [Original local readiness log](evidence/terraform-local-readiness.txt).

Official form: **Student action — excluded from this task**.
