#!/usr/bin/env bash
# update.sh — Pull latest code and restart the GIRA scraper timers.
#
# Run as gira user: bash deploy/update.sh
#   (or via CI: ssh gira@<VPS_IP> 'cd /opt/gira-watcher && bash deploy/update.sh')
#
# Idempotent — safe to run repeatedly.
set -euo pipefail

INSTALL_DIR="/opt/gira-watcher"

cd "$INSTALL_DIR"

# ---------------------------------------------------------------------------
# 1. Pull latest code
# ---------------------------------------------------------------------------
echo ">>> Pulling latest code..."
git pull origin main

# ---------------------------------------------------------------------------
# 2. Sync scraper dependencies
# ---------------------------------------------------------------------------
echo ">>> Syncing scraper dependencies..."
cd packages/scraper
/usr/local/bin/uv sync
cd "$INSTALL_DIR"

# ---------------------------------------------------------------------------
# 3. Update GIRA_COMMIT_SHA in .env
#    Note: git rev-parse output is hex-only — safe for sed substitution.
# ---------------------------------------------------------------------------
NEW_SHA=$(git rev-parse HEAD)
echo ">>> Updating GIRA_COMMIT_SHA to $NEW_SHA..."
if grep -q '^GIRA_COMMIT_SHA=' "$INSTALL_DIR/.env"; then
    sed -i "s/^GIRA_COMMIT_SHA=.*/GIRA_COMMIT_SHA=$NEW_SHA/" "$INSTALL_DIR/.env"
else
    echo "GIRA_COMMIT_SHA=$NEW_SHA" >> "$INSTALL_DIR/.env"
fi

# ---------------------------------------------------------------------------
# 4. Copy systemd units (unconditionally — simpler than diffing, idempotent)
# ---------------------------------------------------------------------------
echo ">>> Updating systemd units..."
sudo /usr/bin/systemctl stop gira-station.timer gira-detail.timer || true
sudo /usr/bin/cp deploy/systemd/*.timer deploy/systemd/*.service /etc/systemd/system/
sudo /usr/bin/systemctl daemon-reload

# ---------------------------------------------------------------------------
# 5. Restart timers
# ---------------------------------------------------------------------------
echo ">>> Restarting timers..."
sudo /usr/bin/systemctl start gira-station.timer gira-detail.timer

# ---------------------------------------------------------------------------
# 6. Print status
# ---------------------------------------------------------------------------
echo ""
echo "=== Update complete ($(git log -1 --format='%h %s')) ==="
echo ""
/usr/bin/systemctl list-timers 'gira-*' --no-pager
