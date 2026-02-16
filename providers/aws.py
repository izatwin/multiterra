def generate(vm):
    # Map CPU/memory to a basic AWS instance type
    instance_type = "t3.micro" if vm["cpu"] <= 2 else "t3.small"

    public_ip = "true" if vm.get("public", False) else "false"

    return f"""
resource "aws_instance" "{vm["name"]}" {{
  ami           = "ami-12345678"
  instance_type = "{instance_type}"
  associate_public_ip_address = {public_ip}
}}
"""
