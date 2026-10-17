# StockPilot AWS infrastructure

Terraform >=1.14,<2; AWS provider is locked to 6.69.1. Default region `ap-south-1`; EKS 1.35 is within standard support at the implementation date (verify using the [AWS release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html) before a later deployment).

Creates a DNS-enabled VPC, two public and two private subnets across two AZs, internet gateway, one NAT/EIP, routes, EKS API/worker IAM, EKS API access entries, restricted public endpoint plus private endpoint, two AL2023 managed workers, VPC CNI/CoreDNS/kube-proxy/Pod Identity, EBS CSI with its own role, and seven-day cluster logs managed for cleanup. Optional OIDC deployment role trusts only the specified repository's production environment, with EKS DescribeCluster and namespace-scoped edit access.

```bash
cp terraform.tfvars.example terraform.tfvars
# Set restricted admin CIDRs and your stable IAM user/role ARN, not an STS session ARN.
aws sts get-caller-identity
terraform fmt -check -recursive
terraform init -lockfile=readonly
terraform validate
terraform test          # mocked topology only; no AWS resources or credentials
terraform plan -out=stockpilot.tfplan
```

The plan is account-dependent. A mock-provider test is not a real AWS plan. `.tfplan`, state and real variable files are ignored. Local state is adequate for a single-operator demo only; use an encrypted, access-controlled S3 backend with locking for shared use. Back up the state securely so resources can be destroyed.

**Do not apply until the account, exact regional cost estimate, planned duration and cleanup authorization are approved.** Costs include the EKS control plane, two t3.large workers, NAT gateway/data, public IPv4, load balancer, EBS and logging. One NAT reduces demo cost but introduces a single-AZ dependency/cross-AZ data cost. Recalculate current prices in the AWS Pricing Calculator rather than relying on a stale estimate.

After approval only: `terraform apply stockpilot.tfplan`, then run the `configure_kubectl` output. Follow ../docs/DEPLOYMENT.md to install storage, controllers, database Secret, monitoring and the release. An assumed-role caller must set `admin_principal_arn` to the underlying IAM role ARN. Create/reuse an account GitHub OIDC provider separately and pass its ARN if CI deploy is needed; duplicate account-level providers are intentionally avoided.

After collecting demonstration evidence, uninstall application and ingress/monitoring, explicitly delete demo PVCs, verify load balancers/volumes are gone, then run `terraform plan -destroy` and an authorized `terraform destroy`. Check the AWS account for residual load balancers, EBS volumes/snapshots, ENIs and logs. Do not destroy before collecting grading evidence.
