provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "StockPilot"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
data "aws_availability_zones" "available" { state = "available" }
data "aws_caller_identity" "current" {}
