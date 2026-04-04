# -----------------------------------------------------------------------------
# Provider tokens
# -----------------------------------------------------------------------------

variable "hetzner_token" {
  description = "Hetzner Cloud API token"
  type        = string
  sensitive   = true
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token with R2 and DNS permissions"
  type        = string
  sensitive   = true
}

variable "vercel_api_token" {
  description = "Vercel API token (Full Access scope)"
  type        = string
  sensitive   = true
}

variable "github_token" {
  description = "GitHub personal access token with repo and admin:org scope"
  type        = string
  sensitive   = true
}

# -----------------------------------------------------------------------------
# Hetzner VPS
# -----------------------------------------------------------------------------

variable "ssh_public_key" {
  description = "SSH public key content (e.g., contents of ~/.ssh/id_ed25519.pub)"
  type        = string
}

variable "server_type" {
  description = "Hetzner server type"
  type        = string
  default     = "cx23"
}

variable "server_location" {
  description = "Hetzner datacenter location"
  type        = string
  default     = "nbg1"
}

variable "server_image" {
  description = "Hetzner OS image"
  type        = string
  default     = "ubuntu-24.04"
}

# -----------------------------------------------------------------------------
# Cloudflare
# -----------------------------------------------------------------------------

variable "cloudflare_account_id" {
  description = "Cloudflare account ID"
  type        = string
}

variable "cloudflare_zone_id" {
  description = "Cloudflare DNS zone ID"
  type        = string
}

variable "r2_bucket_name" {
  description = "Cloudflare R2 bucket name for Parquet fallback"
  type        = string
  default     = "gira-parquet"
}

# -----------------------------------------------------------------------------
# Vercel
# -----------------------------------------------------------------------------

variable "github_repo" {
  description = "GitHub repository path (owner/repo)"
  type        = string
  default     = "emanuelfrazao/gira-watcher"
}

variable "vercel_project_name" {
  description = "Vercel project name"
  type        = string
  default     = "gira-watcher"
}

variable "vercel_org_id" {
  description = "Vercel organization/team ID"
  type        = string
}

variable "vercel_env_vars" {
  description = "Environment variables to set on the Vercel project"
  type = map(object({
    value  = string
    target = list(string)
  }))
  default = {}
}

# -----------------------------------------------------------------------------
# GitHub
# -----------------------------------------------------------------------------

variable "github_repository" {
  description = "GitHub repository name (without owner)"
  type        = string
  default     = "gira-watcher"
}

# -----------------------------------------------------------------------------
# Secrets passed through to GitHub Actions
# -----------------------------------------------------------------------------

variable "r2_access_key_id" {
  description = "Cloudflare R2 S3-compatible access key ID"
  type        = string
  sensitive   = true
}

variable "r2_secret_access_key" {
  description = "Cloudflare R2 S3-compatible secret access key"
  type        = string
  sensitive   = true
}

variable "motherduck_token" {
  description = "MotherDuck API token for DuckDB cloud writes"
  type        = string
  sensitive   = true
}
