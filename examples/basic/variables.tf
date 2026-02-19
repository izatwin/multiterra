variable "provider" {
  type = string
}

variable "vms" {
  type = map(object({
    cpu       = number
    memory_gb = number
    public_ip = bool
  }))
}

variable "aws_ami" {
  type    = string
  default = "ami-12345678"
}

variable "aws_subnet_id" {
  type    = string
  default = null
}

variable "gcp_image" {
  type    = string
  default = "debian-cloud/debian-11"
}

variable "gcp_zone" {
  type    = string
  default = "us-central1-a"
}

variable "gcp_network" {
  type    = string
  default = "default"
}
