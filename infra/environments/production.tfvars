# Non-secret production values
# Secret values are set via TF_VAR_* environment variables (see ../.env.example)

server_type     = "cx23"
server_location = "nbg1"
server_image    = "ubuntu-24.04"

cloudflare_account_id = "" # Set before first apply — Cloudflare dashboard > Account ID
cloudflare_zone_id    = "" # Set before first apply — Cloudflare dashboard > Zone ID
vercel_org_id         = "" # Set before first apply — Vercel dashboard > Settings > General

r2_bucket_name      = "gira-parquet"
github_repo         = "emanuelfrazao/gira-watcher"
github_repository   = "gira-watcher"
vercel_project_name = "gira-watcher"
