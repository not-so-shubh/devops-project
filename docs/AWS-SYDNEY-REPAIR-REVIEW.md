# Sydney worker repair review — identifier-free summary

Reviewed 18 October 2026 IST against the user's actual CloudShell output and Terraform source `952128e01e9afed9a0349faf7c7b58d04e5a96b5`. This page contains an aggregate review, not the underlying operational transcript. AWS account numbers, ARNs, IP addresses, resource IDs and ASG identifiers are omitted. The detailed transcript, state, tfvars and saved plan remain private.

The user-reported EKS control plane is ACTIVE on Kubernetes 1.35. Worker creation failed because the account rejects the original `t3.large` type under its Free Tier restriction. The failed worker group's Auto Scaling result reports **zero actual instances**. The user's eligibility query reports `m7i-flex.large` as allowed, x86_64, **2 vCPUs and 8192 MiB each**. Its offering is present in all three Sydney AZs, including both existing worker-subnet AZs. A private state backup was made before generating the repair plan.

## Reviewed change scope

**Plan: 6 to add, 1 to change, 1 to destroy.**

| Planned action | Scope |
|---|---|
| One replacement | Replace the tainted, failed worker group using two `m7i-flex.large` workers. This counts as one create and one destroy. |
| Five additional creates | Finish the VPC CNI, kube-proxy, CoreDNS, Pod Identity agent and EBS CSI managed add-ons. |
| One in-place update | Change the existing control plane's restricted operator API allowlist to the current operator IP. |
| Preserved | VPC, four subnets, NAT, Internet gateway, routes, IAM roles/policies and the active EKS control plane. |

The [machine-readable aggregate summary](evidence/aws-sydney-repair-summary.json) contains no account-specific infrastructure identifiers. This reviewed summary is not an independently executed AWS result and does not claim a successful repair apply, Ready workers, application deployment or cleanup.

## Public price calculation

The official [Sydney Linux EC2 price](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Sydney)/Linux/index.json) lists `m7i-flex.large` at **$0.1197 USD per instance-hour**, with offer publication on 15 October 2026. Using two workers and the original NAT, load-balancer, public-IP and storage assumptions, the estimated deployment base becomes **$0.44995/hour**, or **$2.70 for six hours**. Traffic, logs, taxes and runtime/resource differences add costs; account credits and actual billing have not been verified. Eligibility is not a claim that the entire deployment is free.

## Approval boundary

**Explicit approval for the failed-group replacement is pending.** The user's mission requires approval before destroying paid resources. Before applying the reviewed saved repair plan, recheck the account, plan scope, current operator IP and that the failed group still has no actual instances. This approval is separate from final teardown/data-loss approval after collecting evidence. The existing spending authorization and runtime window remain in effect; generating a repair plan does not restart them.

The official assignment form remains **Student action — excluded from this task**.
