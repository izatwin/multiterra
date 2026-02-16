def generate(vm):
    machine_type = "e2-micro" if vm["cpu"] <= 2 else "e2-small"

    access_config = "access_config {{ }}" if vm.get("public", False) else ""

    return f"""
resource "google_compute_instance" "{vm["name"]}" {{
  name         = "{vm["name"]}"
  machine_type = "{machine_type}"
  zone         = "us-central1-a"
  
  boot_disk {{
    initialize_params {{
      image = "debian-cloud/debian-11"
    }}
  }}
  
  network_interface {{
    network = "default"
    {access_config}
  }}
}}
"""
