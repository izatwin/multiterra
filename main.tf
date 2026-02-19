locals {
  aws_instance_type = {
    for name, vm in var.vms :
    name => (
      vm.cpu <= 2 && vm.memory_gb <= 2  ? "t3.small" :
      vm.cpu <= 2 && vm.memory_gb <= 4  ? "t3.medium" :
      vm.cpu <= 2 && vm.memory_gb <= 8  ? "t3.large" :
      vm.cpu <= 4 && vm.memory_gb <= 16 ? "t3.xlarge" :
      "t3.2xlarge"
    )
  }

  gcp_machine_type = {
    for name, vm in var.vms :
    name => (
      vm.cpu <= 2 && vm.memory_gb <= 2  ? "e2-small" :
      vm.cpu <= 2 && vm.memory_gb <= 4  ? "e2-medium" :
      vm.cpu <= 4 && vm.memory_gb <= 16 ? "e2-standard-4" :
      "e2-standard-8"
    )
  }
}

resource "aws_instance" "this" {
  for_each = var.provider == "aws" ? var.vms : {}

  ami           = var.aws_ami
  instance_type = local.aws_instance_type[each.key]

  associate_public_ip_address = each.value.public_ip
  subnet_id                   = var.aws_subnet_id

  tags = {
    Name = each.key
  }
}

resource "google_compute_instance" "this" {
  for_each = var.provider == "gcp" ? var.vms : {}

  name         = each.key
  machine_type = local.gcp_machine_type[each.key]
  zone         = var.gcp_zone

  boot_disk {
    initialize_params {
      image = var.gcp_image
    }
  }

  network_interface {
    network = var.gcp_network

    dynamic "access_config" {
      for_each = each.value.public_ip ? [1] : []
      content {}
    }
  }
}
