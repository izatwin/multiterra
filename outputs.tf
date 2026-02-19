locals {
  aws_instances = var.provider == "aws" ? aws_instance.this : {}
  gcp_instances = var.provider == "gcp" ? google_compute_instance.this : {}
}

output "instance_ids" {
  description = "Map of instance ids keyed by VM name."
  value = var.provider == "aws" ? {
    for name, inst in local.aws_instances : name => inst.id
  } : {
    for name, inst in local.gcp_instances : name => inst.id
  }
}

output "public_ips" {
  description = "Map of public IPs keyed by VM name."
  value = var.provider == "aws" ? {
    for name, inst in local.aws_instances : name => inst.public_ip
  } : {
    for name, inst in local.gcp_instances : name => try(inst.network_interface[0].access_config[0].nat_ip, null)
  }
}

output "private_ips" {
  description = "Map of private IPs keyed by VM name."
  value = var.provider == "aws" ? {
    for name, inst in local.aws_instances : name => inst.private_ip
  } : {
    for name, inst in local.gcp_instances : name => inst.network_interface[0].network_ip
  }
}
