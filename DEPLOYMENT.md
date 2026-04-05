# Deployment Guide

End-to-end guide for provisioning, updating, and tearing down the gira-watcher infrastructure.

## Architecture Overview

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Hetzner VPS    │      │   MotherDuck     │      │    Vercel       │
│  (Ubuntu 24.04) │─────▶│   (DuckDB cloud) │◀─────│  (SvelteKit)   │
│                 │      └──────────────────┘      └─────────────────┘
│  systemd timers │
│  every 5 min    │
│                 │      ┌──────────────────┐
└─────────────────┘      │  Cloudflare R2   │
                         │  (Parquet files)  │
        ▲                └──────────────────┘
        │                        ▲
        │ deploy                 │ fallback write
        │                        │
┌───────────────────┐────────────┘
│  GitHub Actions   │
│  CI/CD + fallback │
│  scraper          │
└───────────────────┘
```

| Component | Technology | Purpose |
|-----------|-----------|---------|
| VPS | Hetzner CX23 | Primary scraper host (systemd timers, every 5 min) |
| Storage | MotherDuck (DuckDB) | Cloud data warehouse for scrape data |
| Fallback storage | Cloudflare R2 | Parquet files when MotherDuck is unavailable |
| Website | Vercel (SvelteKit) | Public dashboard |
| DNS | Cloudflare (optional) | Custom domain for website |
| IaC | OpenTofu + R2 state backend | Infrastructure as Code |
| CI/CD | GitHub Actions | Build, test, deploy pipelines |

## Prerequisites

### Tools

- [OpenTofu](https://opentofu.org/) >= 1.8.0
- [just](https://github.com/casey/just) (optional, for convenience recipes)
- [GitHub CLI](https://cli.github.com/) (`gh`)
- SSH client with `ssh-keygen`

### Accounts

| Service | What you need | Where to get it |
|---------|--------------|-----------------|
| [Hetzner Cloud](https://console.hetzner.cloud/) | API token (Read & Write) | Console → Security → API Tokens |
| [Cloudflare](https://dash.cloudflare.com/) | API token + Account ID | Dashboard → Manage Account → API Tokens |
| [Vercel](https://vercel.com/) | API token + Org/Team ID | Settings → Tokens / Settings → General |
| [GitHub](https://github.com/) | Personal Access Token | Settings → Developer Settings → Fine-grained PATs |
| [MotherDuck](https://motherduck.com/) | API token | Settings → API Tokens |
| GIRA (Lisbon) | Account email + password | Personal GIRA account for API access |

### Token permissions

| Token | Required permissions |
|-------|---------------------|
| Hetzner | **Read & Write** (not read-only) |
| Cloudflare | Account > R2: Edit; Zone > DNS: Edit (if using custom domain) |
| Vercel | Full Access scope |
| GitHub PAT | Repository: Read & Write (contents, actions, environments, secrets, administration) |
| MotherDuck | Read & Write |

## Initial Deployment

### 1. Generate SSH key

```bash
ssh-keygen -t ed25519 -C "gira-watcher" -f ~/.ssh/gira-watcher -N ""
```

### 2. Create the R2 state bucket

The OpenTofu state is stored in a Cloudflare R2 bucket. This bucket must exist before `tofu init`.

1. Enable R2 in the Cloudflare dashboard (R2 Object Storage → Get Started)
2. Create the state bucket:
   ```bash
   npx wrangler r2 bucket create tofu-state
   ```
3. Create an R2 API token in Cloudflare dashboard → R2 → Manage R2 API Tokens → Create API Token (Object Read & Write, apply to all buckets)

### 3. Configure environment

```bash
cd infra
cp .env.example .env
```

Fill in all values in `infra/.env`:

```bash
# Provider tokens
TF_VAR_hetzner_token=""              # Hetzner Cloud API token (Read & Write)
TF_VAR_cloudflare_api_token=""       # Cloudflare API token (R2 + DNS)
TF_VAR_vercel_api_token=""           # Vercel API token (Full Access)
TF_VAR_github_token=""               # GitHub PAT

# Hetzner VPS
TF_VAR_ssh_public_key=""             # Contents of ~/.ssh/gira-watcher.pub

# Cloudflare
TF_VAR_cloudflare_account_id=""      # Cloudflare dashboard → Account ID (sidebar)
TF_VAR_cloudflare_zone_id=""         # Leave empty if not using a custom domain

# Vercel
TF_VAR_vercel_org_id=""              # Vercel → Settings → General → Team ID

# Secrets passed through to GitHub Actions
TF_VAR_r2_access_key_id=""           # R2 API token access key
TF_VAR_r2_secret_access_key=""       # R2 API token secret key
TF_VAR_motherduck_token=""           # MotherDuck API token

# R2 backend credentials (same as R2 keys above)
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
```

### 4. Set GitHub secrets

The infrastructure workflow needs secrets to run. Set them before the first apply:

```bash
source infra/.env

# Secrets used by infra-apply.yml
gh secret set HETZNER_TOKEN       --body "$TF_VAR_hetzner_token"
gh secret set CLOUDFLARE_API_TOKEN --body "$TF_VAR_cloudflare_api_token"
gh secret set CLOUDFLARE_ACCOUNT_ID --body "$TF_VAR_cloudflare_account_id"
gh secret set VERCEL_TOKEN        --body "$TF_VAR_vercel_api_token"
gh secret set VERCEL_ORG_ID       --body "$TF_VAR_vercel_org_id"
gh secret set GH_PAT              --body "$TF_VAR_github_token"
gh secret set SSH_PUBLIC_KEY      --body "$TF_VAR_ssh_public_key"
gh secret set R2_ACCESS_KEY       --body "$TF_VAR_r2_access_key_id"
gh secret set R2_SECRET_KEY       --body "$TF_VAR_r2_secret_access_key"
gh secret set MOTHERDUCK_TOKEN    --body "$TF_VAR_motherduck_token"
```

### 5. Provision infrastructure

Run via GitHub Actions (recommended):

```bash
# Preview changes
gh workflow run "Infrastructure" -f action=plan
gh run list --workflow=infra-apply.yml --limit 1

# Apply
gh workflow run "Infrastructure" -f action=apply
gh run watch $(gh run list --workflow=infra-apply.yml --limit 1 --json databaseId -q '.[0].databaseId')
```

Or locally (requires `source infra/.env` first):

```bash
cd infra
just init-remote   # Initialize with R2 backend
just plan          # Preview changes
just apply         # Apply changes
```

This creates 13 resources:
- Hetzner: VPS, SSH key, firewall
- Cloudflare: R2 bucket (+ DNS record if zone_id is set)
- Vercel: project
- GitHub: branch protection, production environment, 8 action secrets (VPS_HOST, R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID, MOTHERDUCK_TOKEN)

### 6. Set the VPS SSH private key secret

This secret is set manually — the private key must never flow through tofu state:

```bash
gh secret set VPS_SSH_KEY < ~/.ssh/gira-watcher
```

### 7. Bootstrap the VPS

Get the VPS IP from the apply output, then run the setup script:

```bash
# With automatic .env population — env vars must be inside the SSH command
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> \
  "GIRA_STORAGE_TOKEN='<motherduck-token>' \
   GIRA_API_EMAIL='<your-gira-email>' \
   GIRA_API_PASSWORD='<your-gira-password>' \
   bash -s" < deploy/setup.sh
```

The setup script:
1. Installs git, curl, uv
2. Creates a `gira` system user with limited sudo
3. Clones the repo to `/opt/gira-watcher`
4. Installs scraper Python dependencies
5. Creates `/opt/gira-watcher/.env` and populates secrets from environment
6. Installs and enables systemd timers (station + detail, every 5 min)

Set up SSH access for the `gira` user (used by deploy workflows):

```bash
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> \
  "mkdir -p /opt/gira-watcher/.ssh && \
   cp /root/.ssh/authorized_keys /opt/gira-watcher/.ssh/authorized_keys && \
   chown -R gira:gira /opt/gira-watcher/.ssh && \
   chmod 700 /opt/gira-watcher/.ssh && \
   chmod 600 /opt/gira-watcher/.ssh/authorized_keys"
```

### 8. Start the scraper

```bash
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> \
  "systemctl start gira-station.timer gira-detail.timer"
```

### 9. Verify

Run the automated verification script locally (requires `source infra/.env`):

```bash
cd infra
just verify
```

This checks: SSH connectivity (root + gira), R2 read/write, Vercel project, GitHub branch protection + environment + secrets, and scraper `--help`.

Manual checks:

```bash
# SSH connectivity
ssh -i ~/.ssh/gira-watcher gira@<VPS_IP> "whoami"

# Timer status
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> "systemctl list-timers 'gira-*'"

# Scraper test
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> \
  "su gira -c 'cd /opt/gira-watcher/packages/scraper && .venv/bin/python -m scraper.main --help'"
```

## Updating

### Scraper / deploy scripts

Automatic — pushing to `main` with changes in `packages/scraper/` or `deploy/` triggers the **Deploy Scraper** workflow, which:

1. SSHs into the VPS as `gira`
2. Runs `deploy/update.sh` (pulls code, syncs deps, restarts timers)

### Website

Automatic — pushing to `main` with changes in `packages/website/` triggers the **Deploy Website** workflow, which builds and deploys to Vercel.

### Infrastructure

Manual — trigger from GitHub Actions or locally:

```bash
# Via GitHub Actions
gh workflow run "Infrastructure" -f action=plan    # preview
gh workflow run "Infrastructure" -f action=apply   # apply

# Locally
cd infra && source .env
just plan
just apply
```

### Manual VPS update

If the deploy workflow fails or you need to update manually:

```bash
ssh -i ~/.ssh/gira-watcher gira@<VPS_IP> \
  "cd /opt/gira-watcher && bash deploy/update.sh"
```

## Teardown

### 1. Stop the scraper

```bash
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> \
  "systemctl stop gira-station.timer gira-detail.timer && \
   systemctl disable gira-station.timer gira-detail.timer"
```

### 2. Destroy infrastructure

```bash
# Via GitHub Actions — not supported (apply-only workflow)
# Run locally:
cd infra && source .env
just init-remote
tofu destroy -var-file=environments/production.tfvars
```

This destroys the VPS, R2 bucket, Vercel project, and GitHub branch protection / secrets / environment.

### 3. Manual cleanup

These resources are not managed by tofu and must be removed manually:

| Resource | How to remove |
|----------|--------------|
| R2 state bucket (`tofu-state`) | Cloudflare dashboard → R2 → Delete bucket |
| GitHub secrets set manually (`VPS_SSH_KEY`) | `gh secret delete VPS_SSH_KEY` |
| SSH key pair (`~/.ssh/gira-watcher*`) | `rm ~/.ssh/gira-watcher ~/.ssh/gira-watcher.pub` |
| Local `.env` file | `rm infra/.env` |
| MotherDuck database | MotherDuck dashboard → Delete database |

## Systemd Timers

The VPS runs two systemd timer/service pairs:

| Timer | Service | Command | Schedule |
|-------|---------|---------|----------|
| `gira-station.timer` | `gira-station.service` | `python -m scraper.main --run-type station` | Every 5 min |
| `gira-detail.timer` | `gira-detail.service` | `python -m scraper.main --run-type detail` | Every 5 min |

Services run as the `gira` user with security hardening (NoNewPrivileges, ProtectSystem=strict, ProtectHome, PrivateTmp). Timeout: 240 seconds.

Common commands (run on VPS as root):

```bash
systemctl list-timers 'gira-*'                    # Show timer schedule
systemctl status gira-station.service              # Last run status
journalctl -u gira-station.service --since "1h ago"  # Recent logs
systemctl restart gira-station.timer               # Restart a timer
systemctl stop gira-station.timer gira-detail.timer   # Stop all
```

## GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI** (`ci.yml`) | Push to main, PRs | Lint, type-check, test (scraper, website, infra, db, deploy) |
| **Deploy Scraper** (`deploy-scraper.yml`) | Push to main (scraper/deploy changes) | SSH + `update.sh` on VPS |
| **Deploy Website** (`deploy-website.yml`) | Push to main (website changes) | Build + deploy to Vercel |
| **Infrastructure** (`infra-apply.yml`) | Manual (workflow_dispatch) | `tofu plan` or `tofu apply` |
| **Scrape Fallback** (`scrape-fallback.yml`) | Every 5 min (cron) | Fallback scraper via R2 (placeholder) |
| **Release** (`release.yml`) | Tag push (`v*.*.*`) | Generate changelog + GitHub Release |

## GitHub Secrets Reference

Secrets managed by tofu (set automatically on `tofu apply`):

| Secret | Source |
|--------|--------|
| `VPS_HOST` | Hetzner VPS IPv4 |
| `R2_ENDPOINT` | Cloudflare R2 endpoint URL |
| `R2_ACCESS_KEY` | Cloudflare R2 access key |
| `R2_SECRET_KEY` | Cloudflare R2 secret key |
| `VERCEL_TOKEN` | Vercel API token |
| `VERCEL_ORG_ID` | Vercel team/org ID |
| `VERCEL_PROJECT_ID` | Vercel project ID |
| `MOTHERDUCK_TOKEN` | MotherDuck API token |

Secrets set manually:

| Secret | Source | Used by |
|--------|--------|---------|
| `VPS_SSH_KEY` | `~/.ssh/gira-watcher` (private key) | Deploy Scraper |
| `HETZNER_TOKEN` | Hetzner API token | Infrastructure |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API token | Infrastructure |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID | Infrastructure |
| `GH_PAT` | GitHub PAT | Infrastructure |
| `SSH_PUBLIC_KEY` | `~/.ssh/gira-watcher.pub` | Infrastructure |

## VPS Filesystem Layout

```
/opt/gira-watcher/
├── .env                     # Runtime secrets (0640, gira:gira)
├── .ssh/authorized_keys     # SSH access for gira user
├── packages/
│   └── scraper/
│       └── .venv/           # Python virtualenv (managed by uv)
└── deploy/
    ├── setup.sh             # Initial bootstrap (run as root)
    ├── update.sh            # Pull + restart (run as gira)
    ├── .env.template        # Template for .env
    └── systemd/
        ├── gira-station.timer
        ├── gira-station.service
        ├── gira-detail.timer
        └── gira-detail.service

/etc/systemd/system/
├── gira-station.timer       # Copied from deploy/systemd/
├── gira-station.service
├── gira-detail.timer
└── gira-detail.service

/etc/sudoers.d/gira-scraper  # Limited sudo for gira user
```

## Troubleshooting

### Tofu apply fails with "Mismatch between input and plan variable value"

Secret-sourced variables (set via `TF_VAR_*` env vars) must **not** also appear in `production.tfvars`. Remove any duplicate entries from the tfvars file.

### Tofu apply fails with "project already exists" (Vercel)

The Vercel project was created outside of tofu. Either delete it from the Vercel dashboard and re-apply, or import it:

```bash
tofu import module.vercel.vercel_project.website <project-id>
```

### SSH connection refused on fresh VPS

The VPS takes 30–90 seconds to boot and initialize SSH. The `verify.sh` script handles this with exponential backoff. Wait and retry.

### Deploy Scraper workflow fails with "Permission denied"

Ensure the `gira` user has SSH access:
```bash
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> \
  "cp /root/.ssh/authorized_keys /opt/gira-watcher/.ssh/authorized_keys && \
   chown gira:gira /opt/gira-watcher/.ssh/authorized_keys"
```

### uv not found on VPS

The setup script copies `uv` to `/usr/local/bin/`. If it's missing:
```bash
ssh -i ~/.ssh/gira-watcher root@<VPS_IP> \
  "curl -LsSf https://astral.sh/uv/install.sh | sh && \
   cp /root/.local/bin/uv /usr/local/bin/uv && \
   chmod 755 /usr/local/bin/uv"
```
