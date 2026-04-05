# -----------------------------------------------------------------------------
# Provider configuration
# -----------------------------------------------------------------------------

provider "hcloud" {
  token = var.hetzner_token
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

provider "vercel" {
  api_token = var.vercel_api_token
}

provider "github" {
  token = var.github_token
}

# -----------------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------------

module "hetzner" {
  source = "./modules/hetzner"

  ssh_public_key = var.ssh_public_key
  server_type    = var.server_type
  location       = var.server_location
  image          = var.server_image
}

module "cloudflare" {
  source = "./modules/cloudflare"

  cloudflare_account_id = var.cloudflare_account_id
  r2_bucket_name        = var.r2_bucket_name
  zone_id               = var.cloudflare_zone_id
  vps_ipv4              = module.hetzner.server_ipv4
}

module "vercel" {
  source = "./modules/vercel"

  project_name          = var.vercel_project_name
  framework             = "sveltekit"
  environment_variables = var.vercel_env_vars
}

module "github" {
  source = "./modules/github"

  repository                = var.github_repository
  branch_protection_pattern = "main"
  required_status_checks    = ["ci-gate"]

  secrets = {
    VPS_HOST = module.hetzner.server_ipv4
    # VPS_SSH_KEY is set manually — private key must not flow through Tofu state
    R2_ENDPOINT       = module.cloudflare.r2_endpoint
    R2_ACCESS_KEY     = var.r2_access_key_id
    R2_SECRET_KEY     = var.r2_secret_access_key
    VERCEL_TOKEN      = var.vercel_api_token
    VERCEL_ORG_ID     = var.vercel_org_id
    VERCEL_PROJECT_ID = module.vercel.project_id
    MOTHERDUCK_TOKEN  = var.motherduck_token
  }
}
