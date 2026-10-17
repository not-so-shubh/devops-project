resource "aws_iam_role" "github_deploy" {
  count = var.github_oidc_provider_arn != "" ? 1 : 0
  name  = "${var.cluster_name}-github-deploy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Federated = var.github_oidc_provider_arn }
      Action    = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          "token.actions.githubusercontent.com:sub" = "repo:${var.github_repository}:environment:production"
        }
      }
    }]
  })
}
resource "aws_iam_role_policy" "github_deploy" {
  count = length(aws_iam_role.github_deploy)
  role  = aws_iam_role.github_deploy[0].id
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = ["eks:DescribeCluster"], Resource = aws_eks_cluster.main.arn }]
  })
}
resource "aws_eks_access_entry" "github_deploy" {
  count         = length(aws_iam_role.github_deploy)
  cluster_name  = aws_eks_cluster.main.name
  principal_arn = aws_iam_role.github_deploy[0].arn
}
resource "aws_eks_access_policy_association" "github_deploy" {
  count         = length(aws_iam_role.github_deploy)
  cluster_name  = aws_eks_cluster.main.name
  principal_arn = aws_eks_access_entry.github_deploy[0].principal_arn
  policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy"
  access_scope {
    type       = "namespace"
    namespaces = ["stockpilot"]
  }
}
