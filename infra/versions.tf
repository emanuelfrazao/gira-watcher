terraform {
  required_version = ">= 1.8.0"

  backend "s3" {
    bucket = "tofu-state"
    key    = "gira-watcher/terraform.tfstate"
    region = "auto"

    endpoints = {
      s3 = "https://67df74dd89804fe6a6a3825e1d825870.r2.cloudflarestorage.com"
    }

    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
    use_lockfile                = true
  }

  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.60"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.17"
    }
    vercel = {
      source  = "vercel/vercel"
      version = "~> 4.6"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.11"
    }
  }
}
