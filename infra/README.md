# Infrastructure

OpenTofu modules for provisioning all cloud resources: Hetzner VPS, Cloudflare R2, Vercel hosting, and GitHub repo settings.

## Prerequisites

- [OpenTofu](https://opentofu.org/) >= 1.8.0
- [just](https://github.com/casey/just) (optional, for recipe shortcuts)
- Cloudflare R2 state bucket created manually (one-time setup)

## State Backend Setup (One-Time)

The OpenTofu state is stored in a Cloudflare R2 bucket via the S3 backend.

1. Create the state bucket:

   ```bash
   wrangler r2 bucket create tofu-state
   ```

2. Create an R2 API token for S3 access:

   - Go to Cloudflare Dashboard > R2 > Manage R2 API Tokens
   - Create a token with read/write access to the `tofu-state` bucket
   - Note the Access Key ID and Secret Access Key

3. Update `versions.tf` — replace `CLOUDFLARE_ACCOUNT_ID` in the backend endpoint URL with your actual Cloudflare account ID.

4. Copy the env template and fill in values:

   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. Source the environment and initialize:

   ```bash
   source .env
   just init-remote
   ```

## Usage

```bash
# Preview changes
just plan

# Apply changes
just apply

# Destroy all resources
just destroy
```

## CI Validation (No Backend Required)

```bash
just check
# Runs: tofu init -backend=false && tofu fmt -check && tofu validate
```

## Modules

| Module | Resources | Purpose |
|--------|-----------|---------|
| `modules/hetzner/` | VPS, SSH key, firewall | Scraper host |
| `modules/cloudflare/` | R2 bucket, DNS record | Parquet fallback, DNS |
| `modules/vercel/` | Project, env vars | Website hosting |
| `modules/github/` | Branch protection, secrets, environments | Repo settings |

## Variables

All secret values are provided via `TF_VAR_*` environment variables. See `.env.example` for the full list.

Non-secret values (server type, location, bucket names) are in `environments/production.tfvars`.

## File Structure

```
infra/
├── main.tf                    # Provider config + module composition
├── variables.tf               # Root input variables
├── outputs.tf                 # VPS IP, R2 URL, Vercel URL
├── versions.tf                # S3/R2 backend + provider pins
├── modules/
│   ├── hetzner/               # VPS, SSH key, firewall, cloud-init
│   ├── cloudflare/            # R2 bucket, DNS record
│   ├── vercel/                # Project, environment variables
│   └── github/                # Branch protection, secrets, environments
├── environments/
│   └── production.tfvars      # Non-secret production values
├── .env.example               # TF_VAR_* secret template
├── justfile                   # Operational recipes
└── README.md                  # This file
```
