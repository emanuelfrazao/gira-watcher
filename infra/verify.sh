#!/usr/bin/env bash
# verify.sh — Verify all cloud resources provisioned by tofu apply.
#
# Prerequisites:
#   - tofu apply has been run (state file populated)
#   - deploy/setup.sh has been run on the VPS
#   - CLI tools authenticated: ssh, wrangler, vercel, gh
#
# Usage: bash verify.sh
set -euo pipefail

# --- Read tofu outputs ---
VPS_IP=$(tofu output -raw vps_ipv4 2>/dev/null) || {
  echo "Error: could not read tofu outputs — ensure 'just apply' has been run from infra/" >&2
  exit 1
}
R2_BUCKET=$(tofu output -raw r2_bucket_name 2>/dev/null) || {
  echo "Error: could not read tofu outputs — ensure 'just apply' has been run from infra/" >&2
  exit 1
}
REPO="emanuelfrazao/gira-watcher"
PROJECT_NAME="gira-watcher"

passed=0
failed=0

check() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "  PASS  $name"
    passed=$((passed + 1))
  else
    echo "  FAIL  $name"
    failed=$((failed + 1))
  fi
}

# wait_for_ssh — retry SSH connection with exponential backoff.
# A fresh Hetzner VPS takes 30-90s to become SSH-accessible after
# tofu apply, so the first connectivity check must tolerate delays.
wait_for_ssh() {
  local user="$1" ip="$2" max_attempts=6 delay=10
  for i in $(seq 1 "$max_attempts"); do
    # StrictHostKeyChecking=accept-new is intentional: on a just-provisioned
    # VPS we trust the host key on first connection. This avoids interactive
    # prompts while still recording the key for future sessions.
    if ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new \
           "${user}@${ip}" exit >/dev/null 2>&1; then
      return 0
    fi
    echo "    Waiting for SSH (attempt $i/$max_attempts, next retry in ${delay}s)..."
    sleep "$delay"
    delay=$((delay * 2))
  done
  return 1
}

echo "=== Verifying provisioned resources ==="
echo ""

# 1. VPS SSH (root) — uses retry for fresh VPS boot delay
echo "--- Hetzner VPS ---"
check "SSH as root" wait_for_ssh root "$VPS_IP"

# 2. VPS SSH (gira user — key provisioned by cloud-init, not setup.sh)
# Uses retry: cloud-init creates the gira user asynchronously, so it may not
# be ready immediately even after root SSH succeeds.
check "SSH as gira" wait_for_ssh gira "$VPS_IP"

# 3. Scraper --help on VPS
check "Scraper --help" ssh -o ConnectTimeout=10 "gira@${VPS_IP}" \
  'cd /opt/gira-watcher/packages/scraper && .venv/bin/python -m scraper.main --help'

# 4. R2 bucket — write, read, and delete a test object.
# Note: wrangler must be authenticated to the correct Cloudflare account.
# If you have multiple accounts, set CLOUDFLARE_ACCOUNT_ID in your environment.
echo ""
echo "--- Cloudflare R2 ---"
check "R2 write test object" wrangler r2 object put "${R2_BUCKET}/_verify_test" \
  --content-type text/plain --pipe <<< "gira-verify-test"
check "R2 read test object" wrangler r2 object get "${R2_BUCKET}/_verify_test" --pipe
check "R2 delete test object" wrangler r2 object delete "${R2_BUCKET}/_verify_test"

# 5. Vercel project
# Note: if you have multiple Vercel teams, set VERCEL_TEAM_ID or use --scope.
echo ""
echo "--- Vercel ---"
check "Vercel project exists" bash -c \
  "vercel project ls 2>/dev/null | grep -q '${PROJECT_NAME}'"

# 6. GitHub
echo ""
echo "--- GitHub ---"
# Note: GitHub is migrating from .contexts (string array) to .checks (object
# array). The tofu resource currently sets contexts; if GitHub deprecates it,
# this filter may need updating to also check .checks[].context.
check "Branch protection active" bash -c \
  "gh api 'repos/${REPO}/branches/main/protection' \
    --jq '.required_status_checks.contexts | index(\"CI / ci-gate\") != null' \
    | grep -q true"
check "Production environment" bash -c \
  "gh api 'repos/${REPO}/environments' \
    --jq '.environments[] | select(.name == \"production\") | .name' \
    | grep -q production"
check "GitHub secret: VPS_HOST" bash -c \
  "gh secret list -R '${REPO}' | grep -q VPS_HOST"
check "GitHub secret: VERCEL_TOKEN" bash -c \
  "gh secret list -R '${REPO}' | grep -q VERCEL_TOKEN"
check "GitHub secret: MOTHERDUCK_TOKEN" bash -c \
  "gh secret list -R '${REPO}' | grep -q MOTHERDUCK_TOKEN"

# --- Summary ---
echo ""
echo "=== Results: ${passed} passed, ${failed} failed ==="
[ "$failed" -eq 0 ] || exit 1
