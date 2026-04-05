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

## End-to-End Provisioning

Complete walkthrough from zero to verified infrastructure and back. Run this as a single session to confirm the full stack works.

### Prerequisites

Before starting, ensure:

- **CLI tools** installed and authenticated: `tofu`, `hcloud`, `wrangler`, `vercel`, `gh`
- **SSH key pair** (ed25519) for VPS access: `ssh-keygen -t ed25519`
- **R2 state bucket** created (one-time — see [State Backend Setup](#state-backend-setup-one-time) above)
- **All credentials** from `.env.example` filled into `.env`

### 1. Environment Setup

```bash
# Replace the placeholder in versions.tf with your Cloudflare account ID
# (one-time — the backend endpoint URL contains CLOUDFLARE_ACCOUNT_ID)
$EDITOR versions.tf

# Fill credentials and source them
cp .env.example .env
$EDITOR .env
source .env
```

### 2. Initialize and Apply

```bash
just init-remote
just apply
```

After `apply` completes, note the VPS IP from the output:

```bash
tofu output -raw vps_ipv4
```

### 3. Bootstrap the VPS

Pipe `deploy/setup.sh` to the new VPS via SSH. The script is idempotent — safe to re-run on partial failure.

```bash
ssh root@$(tofu output -raw vps_ipv4) 'bash -s' < ../deploy/setup.sh
```

Then SSH in to fill the application secrets:

```bash
ssh root@$(tofu output -raw vps_ipv4)
nano /opt/gira-watcher/.env
# Fill MOTHERDUCK_TOKEN and any other application secrets
exit
```

See [`deploy/README.md`](../deploy/README.md) for full VPS operation details.

### 4. Verify

Run the automated verification script to check all provisioned resources:

```bash
just verify
```

This checks: VPS SSH (root + gira), R2 write/read/delete, Vercel project, GitHub branch protection + secrets + environment, and scraper `--help` on VPS.

### 5. Tear Down

```bash
just destroy
```

### 6. Post-Destroy Verification (Manual)

After `just destroy`, confirm resources are gone. These checks are manual because `tofu output` returns empty values after destroy.

```bash
# VPS — should fail with connection refused or timeout
ssh root@<VPS_IP> exit

# R2 — gira-parquet bucket should be absent
wrangler r2 bucket list

# Vercel — gira-watcher project should be absent
vercel project ls

# GitHub — branch protection should return 404
gh api repos/emanuelfrazao/gira-watcher/branches/main/protection
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
├── verify.sh                  # Automated resource verification
└── README.md                  # This file
```
