#!/usr/bin/env bash
# setup.sh — Bootstrap a fresh Ubuntu 24.04 VPS for the GIRA scraper.
#
# Run as root: sudo bash deploy/setup.sh
#
# This script is idempotent — re-running on an already-set-up VPS is safe.
set -euo pipefail

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REPO_URL="https://github.com/emanuelfrazao/gira-watcher.git"
INSTALL_DIR="/opt/gira-watcher"
GIRA_USER="gira"

# ---------------------------------------------------------------------------
# 1. Install system packages
# ---------------------------------------------------------------------------
echo ">>> Installing system packages..."
apt-get update -qq
apt-get install -y -qq git curl

# ---------------------------------------------------------------------------
# 2. Install uv (Python package manager)
# ---------------------------------------------------------------------------
if ! command -v uv &>/dev/null; then
    echo ">>> Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | INSTALLER_NO_MODIFY_PATH=1 sh
    cp "$HOME/.local/bin/uv" /usr/local/bin/uv
    cp "$HOME/.local/bin/uvx" /usr/local/bin/uvx
    chmod 755 /usr/local/bin/uv /usr/local/bin/uvx
else
    echo ">>> uv already installed: $(uv --version)"
fi

# ---------------------------------------------------------------------------
# 3. Create gira system user (no home dir — git clone creates the work dir)
# ---------------------------------------------------------------------------
if ! id "$GIRA_USER" &>/dev/null; then
    echo ">>> Creating system user '$GIRA_USER'..."
    useradd --system --no-create-home --home-dir "$INSTALL_DIR" --shell /bin/bash "$GIRA_USER"
else
    echo ">>> User '$GIRA_USER' already exists."
fi

# ---------------------------------------------------------------------------
# 4. Clone repository (as gira user)
# ---------------------------------------------------------------------------
if [ ! -d "$INSTALL_DIR/.git" ]; then
    echo ">>> Cloning repository into $INSTALL_DIR..."
    mkdir -p "$INSTALL_DIR"
    chown "$GIRA_USER:$GIRA_USER" "$INSTALL_DIR"
    su "$GIRA_USER" -c "git clone $REPO_URL $INSTALL_DIR"
else
    echo ">>> Repository already cloned at $INSTALL_DIR."
fi

# ---------------------------------------------------------------------------
# 5. Configure limited sudo for gira user
# ---------------------------------------------------------------------------
echo ">>> Configuring sudoers for '$GIRA_USER'..."
cat > /etc/sudoers.d/gira-scraper <<'SUDOERS'
gira ALL=(ALL) NOPASSWD: /usr/bin/systemctl daemon-reload, \
    /usr/bin/systemctl restart gira-station.timer, \
    /usr/bin/systemctl restart gira-detail.timer, \
    /usr/bin/systemctl restart gira-station.service, \
    /usr/bin/systemctl restart gira-detail.service, \
    /usr/bin/systemctl start gira-station.timer, \
    /usr/bin/systemctl start gira-detail.timer, \
    /usr/bin/systemctl stop gira-station.timer, \
    /usr/bin/systemctl stop gira-detail.timer, \
    /usr/bin/systemctl status gira-*, \
    /usr/bin/cp /opt/gira-watcher/deploy/systemd/* /etc/systemd/system/
SUDOERS
chmod 0440 /etc/sudoers.d/gira-scraper

# ---------------------------------------------------------------------------
# 6. Install scraper dependencies
# ---------------------------------------------------------------------------
echo ">>> Installing scraper dependencies..."
su "$GIRA_USER" -c "cd $INSTALL_DIR/packages/scraper && /usr/local/bin/uv sync"

# ---------------------------------------------------------------------------
# 7. Create .env from template and populate from environment
# ---------------------------------------------------------------------------
if [ ! -f "$INSTALL_DIR/.env" ]; then
    echo ">>> Creating .env from template..."
    cp "$INSTALL_DIR/deploy/.env.template" "$INSTALL_DIR/.env"
    chown "$GIRA_USER:$GIRA_USER" "$INSTALL_DIR/.env"
    chmod 0640 "$INSTALL_DIR/.env"
else
    echo ">>> .env already exists — skipping template copy."
fi

# Populate .env values from environment variables (if set)
echo ">>> Populating .env from environment..."
git config --global --add safe.directory "$INSTALL_DIR" 2>/dev/null || true
COMMIT_SHA=$(cd "$INSTALL_DIR" && git rev-parse HEAD 2>/dev/null || echo "unknown")
sed -i "s|^GIRA_COMMIT_SHA=.*|GIRA_COMMIT_SHA=$COMMIT_SHA|" "$INSTALL_DIR/.env"

for var in GIRA_STORAGE_TOKEN GIRA_API_EMAIL GIRA_API_PASSWORD; do
    val="${!var:-}"
    if [ -n "$val" ]; then
        sed -i "s|^${var}=.*|${var}=${val}|" "$INSTALL_DIR/.env"
        echo "  Set $var"
    fi
done

# ---------------------------------------------------------------------------
# 8. Install systemd units
# ---------------------------------------------------------------------------
echo ">>> Installing systemd units..."
cp "$INSTALL_DIR/deploy/systemd/"*.timer "$INSTALL_DIR/deploy/systemd/"*.service /etc/systemd/system/
/usr/bin/systemctl daemon-reload

# ---------------------------------------------------------------------------
# 9. Enable timers (do NOT start — operator must fill .env first)
# ---------------------------------------------------------------------------
echo ">>> Enabling timers..."
/usr/bin/systemctl enable gira-station.timer gira-detail.timer

# ---------------------------------------------------------------------------
# 10. Print status and next steps
# ---------------------------------------------------------------------------
echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Fill in secrets:  nano $INSTALL_DIR/.env"
echo "  2. Start timers:     sudo /usr/bin/systemctl start gira-station.timer gira-detail.timer"
echo "  3. Verify:           systemctl list-timers 'gira-*'"
echo ""
