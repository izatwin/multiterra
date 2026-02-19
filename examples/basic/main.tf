terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}

module "vms" {
  source = "../.."

  provider = var.provider
  vms      = var.vms

  aws_ami     = var.aws_ami
  aws_subnet_id = var.aws_subnet_id

  gcp_image   = var.gcp_image
  gcp_zone    = var.gcp_zone
  gcp_network = var.gcp_network
}
