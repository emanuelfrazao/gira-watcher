output "vps_ipv4" {
  description = "Public IPv4 address of the Hetzner VPS"
  value       = module.hetzner.server_ipv4
}

output "r2_bucket_name" {
  description = "Cloudflare R2 bucket name"
  value       = module.cloudflare.r2_bucket_name
}

output "r2_endpoint" {
  description = "Cloudflare R2 S3-compatible endpoint URL"
  value       = module.cloudflare.r2_endpoint
}

output "vercel_project_url" {
  description = "Vercel project URL"
  value       = module.vercel.project_url
}
