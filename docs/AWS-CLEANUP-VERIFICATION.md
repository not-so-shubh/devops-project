# Verified AWS cleanup — 22 October 2026

The user separately approved the reviewed StockPilot teardown and executed [cleanup source `228cccd`](https://github.com/not-so-shubh/devops-project/blob/228cccd843c65b2e9dccbe5452d980a00b889a75/scripts/cleanup-approved-eks.py) in AWS CloudShell. The supplied console output ends with **CLEANUP VERIFIED / PASS** at **05:16:28 IST on 22 October 2026** (23:46:28 UTC on 21 October).

The assistant reviewed the supplied result; it did not operate a direct authenticated AWS session. [Machine-readable result and provenance](evidence/aws-cleanup-summary.json).

## Reviewed scope and execution

The saved Terraform plan contained **33 deletes, no creates or updates**. Its hash, AWS account/region, backup hash, project VPC, cluster, IAM role names, database claim UID, EBS handle and ingress identity were checked before any deletion. The helper's ten safeguard tests passed. A process lock prevents simultaneous cleanup runs.

Traefik and StockPilot were uninstalled first; the approved database claim was explicitly deleted. AWS confirmed the load balancer and database EBS volume were gone while the CSI driver and cluster still existed. Monitoring and metrics-server were then uninstalled. Terraform applied the saved destruction plan and returned success.

The executed Terraform command was `terraform apply <saved-destroy-plan>`, after `terraform plan -destroy -out=...`. This applies the reviewed destruction plan; it is not a fabricated claim that the literal `terraform destroy` command was typed. See the [Terraform plan reference](https://developer.hashicorp.com/terraform/cli/commands/plan).

| Verified result | Actual supplied outcome |
|---|---|
| Terraform-managed resources | 33 destroyed; state empty |
| EKS control plane | Deleted |
| Managed worker group / ASG | Removed |
| Worker instances | Two terminated |
| EBS disks | Database disk and both worker root disks absent; three total |
| Ingress Classic Load Balancer | Deleted |
| VPC / network interfaces | VPC deleted; zero matching network interfaces |
| NAT / Elastic IP | NAT deleted; Elastic IP allocation absent |
| Project IAM roles | Three absent |
| Cluster CloudWatch log group | Absent |

AWS permission failures are not treated as deletion success: only explicit resource-not-found codes or verified empty/terminated results pass the checks.

## Backup and evidence

Before cleanup, the user created a **9,534-byte PostgreSQL custom-format dump**. CloudShell checked its format and readable table-data catalogue. The downloaded/uploaded copy independently matched SHA-256 `cc82758ae8533d5c77d705e61ad8841527c2f6f34e56dd235eff648ec3189ee9`. A full restore rehearsal was not performed.

The database dump, Terraform state/variables/plans, asset IDs and detailed command logs remain private. This public record contains aggregate outcomes and hashes. The [18 October EKS browser/monitoring captures](AWS-EKS-CAPTURE-REVIEW.md) are historical evidence of the deployment before deletion. The old ingress endpoint is no longer a live demo.

The original six-hour approval ended on 18 October; cleanup completed on 22 October. The spending target was not an automatic cutoff. Actual charges and credits have not been checked, and this resource audit does not certify that the entire AWS account has no charges.

## Rubric and remaining work

M7.6 now has actual teardown evidence. The audit records **43 VERIFIED criteria / 94 technical points**, **4 READY FOR DEMO points**, and **2 EXCLUDED form points**. These totals describe technical evidence, not awarded marks.

Use any pre-deletion AWS Console screenshots already saved; missing Console views cannot be reconstructed as genuine AWS screenshots from CLI JSON. Genuine saved terminal output and the private cleanup logs remain available for historical terminal-format evidence. Student security explanation and personal live/accepted recorded presentation remain required. Automatic EKS deployment remains blocked by the documented account OIDC policy. Official form: **Student action — excluded from this task.**
