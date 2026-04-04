output "server_ipv4" {
  description = "Public IPv4 address of the VPS"
  value       = hcloud_server.gira.ipv4_address
}

output "server_id" {
  description = "Hetzner server ID"
  value       = hcloud_server.gira.id
}
