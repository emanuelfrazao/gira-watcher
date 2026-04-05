# Non-secret production values
# Secret values are set via TF_VAR_* environment variables (see ../.env.example)

server_type     = "cx23"
server_location = "nbg1"
server_image    = "ubuntu-24.04"

r2_bucket_name      = "gira-parquet"
github_repo         = "emanuelfrazao/gira-watcher"
github_repository   = "gira-watcher"
vercel_project_name = "gira-watcher"
