variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
variable "cluster_name" {
  type    = string
  default = "stockpilot-eks"
  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z0-9-]{2,35}$", var.cluster_name))
    error_message = "Use a 3–36 character cluster name beginning with a letter."
  }
}
variable "environment" {
  type    = string
  default = "dev"
}
variable "kubernetes_version" {
  description = "EKS standard-support release; confirm regional availability before planning."
  type        = string
  default     = "1.35"
}
variable "admin_cidrs" {
  description = "Public EKS API access allowlist. Replace loopback with your trusted /32 or runner egress CIDRs."
  type        = list(string)
  default     = ["127.0.0.1/32"]
  validation {
    condition     = length(var.admin_cidrs) > 0 && alltrue([for cidr in var.admin_cidrs : can(cidrnetmask(cidr)) && cidr != "0.0.0.0/0"])
    error_message = "Specify valid restricted IPv4 CIDRs; unrestricted API access is disallowed."
  }
}
variable "admin_principal_arn" {
  description = "IAM user/role ARN for the operator, NOT an STS session ARN. Empty uses caller ARN; role sessions must set this explicitly."
  type        = string
  default     = ""
}
variable "node_instance_types" {
  type    = list(string)
  default = ["t3.large"]
}
variable "github_oidc_provider_arn" {
  description = "Existing GitHub OIDC provider ARN. Empty disables CI role creation; avoid duplicate account providers."
  type        = string
  default     = ""
}
variable "github_repository" {
  type    = string
  default = "not-so-shubh/devops-project"
}
