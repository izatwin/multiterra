provider = "aws"

vms = {
  web = {
    cpu       = 2
    memory_gb = 4
    public_ip = true
  }
  worker = {
    cpu       = 4
    memory_gb = 8
    public_ip = false
  }
}
