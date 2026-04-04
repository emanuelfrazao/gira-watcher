resource "hcloud_ssh_key" "deploy" {
  name       = "gira-deploy"
  public_key = var.ssh_public_key
}

resource "hcloud_firewall" "web" {
  name = "gira-web"

  rule {
    description = "Allow SSH"
    direction   = "in"
    protocol    = "tcp"
    port        = "22"
    source_ips  = ["0.0.0.0/0", "::/0"]
  }

  rule {
    description = "Allow HTTP"
    direction   = "in"
    protocol    = "tcp"
    port        = "80"
    source_ips  = ["0.0.0.0/0", "::/0"]
  }

  rule {
    description = "Allow HTTPS"
    direction   = "in"
    protocol    = "tcp"
    port        = "443"
    source_ips  = ["0.0.0.0/0", "::/0"]
  }
}

resource "hcloud_server" "gira" {
  name        = "gira-watcher"
  server_type = var.server_type
  location    = var.location
  image       = var.image

  ssh_keys     = [hcloud_ssh_key.deploy.id]
  firewall_ids = [hcloud_firewall.web.id]

  user_data = templatefile("${path.module}/templates/cloud-init.yml.tftpl", {
    ssh_public_key = var.ssh_public_key
  })

  labels = {
    project = "gira-watcher"
  }
}
