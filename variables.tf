variable "provider" {
  description = "Target cloud provider: aws or gcp."
  type        = string

  validation {
    condition     = contains(["aws", "gcp"], var.provider)
    error_message = "provider must be \"aws\" or \"gcp\"."
  }
}

variable "vms" {
  description = "Map of VM definitions keyed by name."
  type = map(object({
    cpu       = number
    memory_gb = number
    public_ip = bool
  }))
}

variable "aws_ami" {
  description = "AMI to use for AWS instances."
  type        = string
  default     = "ami-12345678"
}

variable "aws_subnet_id" {
  description = "Subnet ID for AWS instances. Null uses provider/default subnet."
  type        = string
  default     = null
}

variable "gcp_image" {
  description = "Image to use for GCP instances."
  type        = string
  default     = "debian-cloud/debian-11"
}

variable "gcp_zone" {
  description = "GCP zone for instances."
  type        = string
  default     = "us-central1-a"
}

variable "gcp_network" {
  description = "GCP network for instances."
  type        = string
  default     = "default"
}
