resource "cloudflare_r2_bucket" "parquet" {
  account_id = var.cloudflare_account_id
  name       = var.r2_bucket_name
  location   = "WEUR"
}

resource "cloudflare_dns_record" "vps" {
  count   = var.zone_id != "" ? 1 : 0
  zone_id = var.zone_id
  name    = "vps"
  type    = "A"
  content = var.vps_ipv4
  ttl     = 300
  proxied = false
}

# TODO: cloudflare_workers_script — deferred until Worker code exists.
# Wrangler handles bundling; Tofu deploys the built artifact.
