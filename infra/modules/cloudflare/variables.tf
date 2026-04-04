variable "cloudflare_account_id" {
  description = "Cloudflare account ID"
  type        = string
}

variable "r2_bucket_name" {
  description = "R2 bucket name for Parquet fallback storage"
  type        = string
  default     = "gira-parquet"
}

variable "zone_id" {
  description = "Cloudflare DNS zone ID"
  type        = string
}

variable "vps_ipv4" {
  description = "VPS IPv4 address for DNS A record"
  type        = string
}
