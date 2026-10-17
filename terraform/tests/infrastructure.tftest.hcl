# Offline topology regression check. This is not evidence of a real AWS plan/apply.
mock_provider "aws" {
  mock_data "aws_availability_zones" {
    defaults = { names = ["ap-south-1a", "ap-south-1b"] }
  }
  mock_data "aws_caller_identity" {
    defaults = {
      arn        = "arn:aws:iam::111122223333:user/terraform-test"
      account_id = "111122223333"
      user_id    = "terraform-test"
    }
  }
}
run "network_and_cluster_topology" {
  command = plan
  assert {
    condition     = length(aws_subnet.public) == 2 && length(aws_subnet.private) == 2
    error_message = "Two public and two private subnets are required."
  }
  assert {
    condition     = aws_eks_node_group.main.scaling_config[0].desired_size == 2
    error_message = "The managed node group must start with two workers."
  }
  assert {
    condition     = aws_eks_cluster.main.vpc_config[0].endpoint_private_access
    error_message = "Private cluster API access must remain available."
  }
}
