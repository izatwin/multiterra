from pathlib import Path

import yaml

from providers import aws, gcp

# Load spec
with Path("spec.yaml").open() as f:
    spec = yaml.safe_load(f)

vm = spec["vm"]

# Generate AWS Terraform
aws_tf = aws.generate(vm)
with Path("generated_aws.tf").open("w") as f:
    f.write(aws_tf)

# Generate GCP Terraform
gcp_tf = gcp.generate(vm)
with Path("generated_gcp.tf").open("w") as f:
    f.write(gcp_tf)

print("Terraform files generated for AWS and GCP!")
