variable "ssh_public_key" {
  description = "SSH public key content (e.g., contents of ~/.ssh/id_ed25519.pub)"
  type        = string
}

variable "server_type" {
  description = "Hetzner server type"
  type        = string
  default     = "cx23"
}

variable "location" {
  description = "Hetzner datacenter location"
  type        = string
  default     = "nbg1"
}

variable "image" {
  description = "Hetzner OS image"
  type        = string
  default     = "ubuntu-24.04"
}
