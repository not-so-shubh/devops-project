output "vpc_id" { value = aws_vpc.main.id }
output "public_subnet_ids" { value = [for s in aws_subnet.public : s.id] }
output "private_subnet_ids" { value = [for s in aws_subnet.private : s.id] }
output "cluster_name" { value = aws_eks_cluster.main.name }
output "cluster_endpoint" { value = aws_eks_cluster.main.endpoint }
output "node_group_name" { value = aws_eks_node_group.main.node_group_name }
output "github_deploy_role_arn" { value = try(aws_iam_role.github_deploy[0].arn, null) }
output "configure_kubectl" {
  value = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.main.name}"
}
