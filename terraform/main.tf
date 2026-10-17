locals {
  azs = slice(data.aws_availability_zones.available.names, 0, 2)
  subnets = {
    a = { az = local.azs[0], public = "10.42.101.0/24", private = "10.42.1.0/24" }
    b = { az = local.azs[1], public = "10.42.102.0/24", private = "10.42.2.0/24" }
  }
}
resource "aws_vpc" "main" {
  cidr_block           = "10.42.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags                 = { Name = "${var.cluster_name}-vpc" }
}
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}
resource "aws_subnet" "public" {
  for_each          = local.subnets
  vpc_id            = aws_vpc.main.id
  availability_zone = each.value.az
  cidr_block        = each.value.public
  tags = {
    Name                     = "${var.cluster_name}-public-${each.key}"
    "kubernetes.io/role/elb" = "1"
  }
}
resource "aws_subnet" "private" {
  for_each          = local.subnets
  vpc_id            = aws_vpc.main.id
  availability_zone = each.value.az
  cidr_block        = each.value.private
  tags = {
    Name                              = "${var.cluster_name}-private-${each.key}"
    "kubernetes.io/role/internal-elb" = "1"
  }
}
resource "aws_eip" "nat" { domain = "vpc" }
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public["a"].id
  depends_on    = [aws_internet_gateway.main]
}
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }
}
resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}
resource "aws_route_table_association" "private" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}
resource "aws_iam_role" "cluster" {
  name = "${var.cluster_name}-cluster"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "eks.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}
resource "aws_iam_role_policy_attachment" "cluster" {
  role       = aws_iam_role.cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version
  access_config {
    authentication_mode                         = "API"
    bootstrap_cluster_creator_admin_permissions = false
  }
  upgrade_policy { support_type = "STANDARD" }
  enabled_cluster_log_types = ["api", "audit", "authenticator"]
  vpc_config {
    subnet_ids              = [for s in aws_subnet.private : s.id]
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = var.admin_cidrs
  }
  depends_on = [aws_iam_role_policy_attachment.cluster]
}
resource "aws_eks_access_entry" "admin" {
  cluster_name  = aws_eks_cluster.main.name
  principal_arn = var.admin_principal_arn != "" ? var.admin_principal_arn : data.aws_caller_identity.current.arn
}
resource "aws_eks_access_policy_association" "admin" {
  cluster_name  = aws_eks_cluster.main.name
  principal_arn = aws_eks_access_entry.admin.principal_arn
  policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
  access_scope { type = "cluster" }
}
resource "aws_iam_role" "nodes" {
  name = "${var.cluster_name}-nodes"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "ec2.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}
resource "aws_iam_role_policy_attachment" "nodes" {
  for_each   = toset(["AmazonEKSWorkerNodePolicy", "AmazonEC2ContainerRegistryPullOnly", "AmazonEKS_CNI_Policy"])
  role       = aws_iam_role.nodes.name
  policy_arn = "arn:aws:iam::aws:policy/${each.key}"
}
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "operations"
  node_role_arn   = aws_iam_role.nodes.arn
  subnet_ids      = [for s in aws_subnet.private : s.id]
  instance_types  = var.node_instance_types
  ami_type        = "AL2023_x86_64_STANDARD"
  capacity_type   = "ON_DEMAND"
  disk_size       = 30
  scaling_config {
    min_size     = 2
    max_size     = 4
    desired_size = 2
  }
  update_config { max_unavailable = 1 }
  depends_on = [aws_iam_role_policy_attachment.nodes, aws_route_table_association.private]
}
resource "aws_eks_addon" "network" {
  for_each     = toset(["vpc-cni", "kube-proxy", "coredns", "eks-pod-identity-agent"])
  cluster_name = aws_eks_cluster.main.name
  addon_name   = each.value
  depends_on   = [aws_eks_node_group.main]
}
# EBS CSI uses Pod Identity rather than broad EBS permissions on every node.
resource "aws_iam_role" "ebs" {
  name = "${var.cluster_name}-ebs-csi"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "pods.eks.amazonaws.com" }, Action = ["sts:AssumeRole", "sts:TagSession"] }]
  })
}
resource "aws_iam_role_policy_attachment" "ebs" {
  role       = aws_iam_role.ebs.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
}
resource "aws_eks_pod_identity_association" "ebs" {
  cluster_name    = aws_eks_cluster.main.name
  namespace       = "kube-system"
  service_account = "ebs-csi-controller-sa"
  role_arn        = aws_iam_role.ebs.arn
}
resource "aws_eks_addon" "ebs" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "aws-ebs-csi-driver"
  depends_on   = [aws_eks_addon.network, aws_iam_role_policy_attachment.ebs, aws_eks_pod_identity_association.ebs]
}
