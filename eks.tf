provider "aws" {
  region = "us-west-2"
}

# Creación de un VPC
resource "aws_vpc" "example" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "k8s-vpc"
  }
}

# Creación de subredes privadas
resource "aws_subnet" "private_a" {
  cidr_block = "10.0.1.0/24"
  vpc_id     = aws_vpc.example.id

  tags = {
    Name = "k8s-private-a"
  }
}

resource "aws_subnet" "private_b" {
  cidr_block = "10.0.2.0/24"
  vpc_id     = aws_vpc.example.id

  tags = {
    Name = "k8s-private-b"
  }
}

# Creación de subredes públicas
resource "aws_subnet" "public_a" {
  cidr_block = "10.0.101.0/24"
  vpc_id     = aws_vpc.example.id

  tags = {
    Name = "k8s-public-a"
  }
}

resource "aws_subnet" "public_b" {
  cidr_block = "10.0.102.0/24"
  vpc_id     = aws_vpc.example.id

  tags = {
    Name = "k8s-public-b"
  }
}

# Creación del cluster de Kubernetes
resource "aws_eks_cluster" "k8s" {
  name     = "k8s-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  vpc_config = {
    subnet_ids = [
      aws_subnet.private_a.id,
      aws_subnet.private_b.id,
      aws_subnet.public_a.id,
      aws_subnet.public_b.id,
    ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster,
  ]
}

# Creación del rol IAM para el cluster de Kubernetes
resource "aws_iam_role" "eks_cluster" {
  name = "eks-cluster"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

# Adjuntar políticas al rol IAM del cluster de Kubernetes
resource "aws_iam_role_policy_attachment" "eks_cluster" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSCluster
