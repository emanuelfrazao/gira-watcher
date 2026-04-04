# VPS Deployment

Systemd timer/service units and shell scripts for running the GIRA scraper on a Hetzner VPS (Ubuntu 24.04 LTS).

## Prerequisites

- Hetzner CX23 VPS (or equivalent) running Ubuntu 24.04 LTS
- Root SSH access
- Network connectivity to GitHub, MotherDuck, and the GIRA API

## Filesystem Layout

After setup, the VPS filesystem looks like:

```
/opt/gira-watcher/              # Git checkout (owned by gira:gira)
├── .env                        # Secrets (0640, gira:gira, not in git)
├── packages/scraper/
│   ├── .venv/                  # Python virtualenv (created by uv sync)
│   └── src/scraper/main.py     # Entrypoint
└── deploy/
    ├── systemd/                # Unit files (copied to /etc/systemd/system/)
    ├── setup.sh
    ├── update.sh
    └── .env.template
```

## First-Time Setup

1. SSH into the VPS as root:

   ```bash
   ssh root@<VPS_IP>
   ```

2. Download and run the setup script:

   ```bash
   curl -LsSf https://raw.githubusercontent.com/emanuelfrazao/gira-watcher/main/deploy/setup.sh | bash
   ```

   Or, if the repo is already cloned:

   ```bash
   bash /opt/gira-watcher/deploy/setup.sh
   ```

   The script will:
   - Install system packages (`git`, `curl`)
   - Install [uv](https://docs.astral.sh/uv/) to `/usr/local/bin/`
   - Create a `gira` system user with limited sudo privileges
   - Clone the repository into `/opt/gira-watcher/`
   - Install scraper Python dependencies
   - Create `.env` from the template
   - Install and enable systemd timer units

3. Fill in the secrets:

   ```bash
   nano /opt/gira-watcher/.env
   ```

   See [Environment Variables](#environment-variables) below for descriptions.

4. Start the timers:

   ```bash
   sudo /usr/bin/systemctl start gira-station.timer gira-detail.timer
   ```

5. Verify:

   ```bash
   systemctl list-timers 'gira-*'
   ```

## Routine Updates

To deploy the latest code, run as the `gira` user:

```bash
bash /opt/gira-watcher/deploy/update.sh
```

This pulls the latest code, syncs dependencies, updates the commit SHA in `.env`, copies any changed systemd units, and restarts the timers.

From CI (future deploy workflow):

```bash
ssh gira@<VPS_IP> 'cd /opt/gira-watcher && bash deploy/update.sh'
```

## Timer Management

### Start / Stop

```bash
# Start both timers
sudo /usr/bin/systemctl start gira-station.timer gira-detail.timer

# Stop both timers
sudo /usr/bin/systemctl stop gira-station.timer gira-detail.timer
```

### Check Status

```bash
# List active timers
systemctl list-timers 'gira-*'

# Detailed timer status
systemctl status gira-station.timer
systemctl status gira-detail.timer
```

### Change Cadence

Edit the `OnCalendar=` directive in `deploy/systemd/gira-station.timer` or `gira-detail.timer`, then run `update.sh` to apply.

Examples:
- Every 5 minutes: `OnCalendar=*:0/5`
- Every 2 minutes: `OnCalendar=*:0/2`
- Stagger detail by 1 minute: `OnCalendar=*:1/5` (fires at :01, :06, :11, ...)

### Run Manually

```bash
sudo /usr/bin/systemctl start gira-station.service
sudo /usr/bin/systemctl start gira-detail.service
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GIRA_STORAGE_URL` | Yes | MotherDuck connection URL (e.g., `md:gira`) |
| `GIRA_STORAGE_TOKEN` | Yes | MotherDuck write token |
| `GIRA_API_EMAIL` | Yes (detail) | GIRA account email for authenticated endpoints |
| `GIRA_API_PASSWORD` | Yes (detail) | GIRA account password |
| `GIRA_SCHEDULER_IDENTITY` | Yes | Identifies the scheduler (`vps-systemd`) |
| `GIRA_COMMIT_SHA` | Auto | Set automatically by `update.sh` |
| `GITHUB_AUDIT_TOKEN` | No | GitHub PAT for audit repo dispatch |
| `GITHUB_AUDIT_REPO` | No | Audit repository (e.g., `user/gira-watcher-audit`) |

## Troubleshooting

### Timer not firing

```bash
# Check if timer is active
systemctl is-active gira-station.timer

# Check if timer is enabled (survives reboot)
systemctl is-enabled gira-station.timer

# Check timer schedule details
systemctl show gira-station.timer --property=NextElapseUSecRealtime
```

### Service failing

```bash
# Check exit status
systemctl status gira-station.service

# View recent logs
journalctl -u gira-station.service -n 50 --no-pager

# View logs since last boot
journalctl -u gira-station.service -b
```

### Common issues

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `(code=exited, status=1)` | Missing or invalid `.env` values | Check `nano /opt/gira-watcher/.env` |
| `(code=exited, status=203)` | Python venv missing or broken | Run `cd /opt/gira-watcher/packages/scraper && /usr/local/bin/uv sync` |
| Timer shows `n/a` for next fire | Timer not started | `sudo /usr/bin/systemctl start gira-station.timer` |
| `Permission denied` on `.env` | Wrong file permissions | `chmod 0640 /opt/gira-watcher/.env && chown gira:gira /opt/gira-watcher/.env` |

## Logs

View scraper output with `journalctl`:

```bash
# Station scraper logs (last 50 lines)
journalctl -u gira-station.service -n 50 --no-pager

# Detail scraper logs (last 50 lines)
journalctl -u gira-detail.service -n 50 --no-pager

# Follow logs in real time
journalctl -u gira-station.service -f

# Logs from a specific time range
journalctl -u gira-station.service --since "2024-01-01 12:00" --until "2024-01-01 13:00"
```
