# multiterra

An opinionated wrapper for pulumi to generate configs for various providers using a single spec file.

Providers to start out supporting: AWS, GCP

### Inputs

- `provider`: "aws" or "gcp"
- `vms`: map of VM definitions keyed by name
  - `cpu` (number)
  - `memory_gb` (number)
  - `public_ip` (bool)
- `aws_ami` (string, default "ami-12345678")
- `aws_subnet_id` (string, default null)
- `gcp_image` (string, default "debian-cloud/debian-11")
- `gcp_zone` (string, default "us-central1-a")
- `gcp_network` (string, default "default")

### Outputs

- `instance_ids`: map of instance IDs
- `public_ips`: map of public IPs
- `private_ips`: map of private IPs

### Example

See `examples/basic` for a working example. Update provider credentials/IDs as needed.
