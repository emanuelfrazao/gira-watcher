# GIRA Watch

Transparent public accountability for Lisbon's shared bicycle system.

GIRA Watch collects, stores, and analyses real-time availability data from the GIRA municipal bicycle network, using the same API that GIRA's own mobile app uses. Every line of code, every deployment step, and every raw data point is public and reproducible.

## What this project does

GIRA operates under a public concession in Lisbon. Residents widely report persistent station emptiness and bikes that cannot be released -- but no systematic evidence exists to confirm or refute this. GIRA Watch produces that evidence: a continuous, 5-minute-resolution time-series of station availability across all ~200 docking stations, analysed against five pre-registered metrics.

The methodology is committed to this repository before any data collection begins, so the findings cannot be cherry-picked after the fact.

## How it works

A VPS-based scheduler (systemd timer) runs the scraper every 5 minutes as the primary data collection path. A GitHub Actions cron workflow provides a fallback writer. The scraper fetches all station states from the GIRA API, validates the response, and writes to a normalized DuckDB schema in MotherDuck. The fallback writer exports Parquet snapshots to Cloudflare R2. A SvelteKit website deployed on Vercel reads from MotherDuck and renders the five pre-registered metrics.

```
GIRA API
  -> packages/scraper/     (VPS primary, every 5 min)
  -> MotherDuck            (normalized DuckDB schema)
  -> packages/website/     (SvelteKit on Vercel)

GIRA API
  -> .github/workflows/    (GitHub Actions fallback)
  -> Cloudflare R2         (Parquet snapshots)
```

Every scrape run is logged with its commit SHA and run URL, creating a public, auditable chain of custody from source code to stored data.

## Quick start

```bash
# Prerequisites: uv, node + npm, just, duckdb (optional)

# Database schema
cd packages/db
just seed               # Apply migrations + load test fixtures

# Scraper (Python)
cd packages/scraper
uv sync --all-extras
just check              # Lint + typecheck + test

# Website (SvelteKit)
cd packages/website
npm install
just dev                # Start development server
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full development guide.

## Accessing the data

The full dataset is publicly queryable. Attach it directly in any DuckDB shell:

```sql
-- Share URL will be published here once collection is live
ATTACH '...' AS gira (READ_ONLY);
SELECT * FROM gira.observations LIMIT 10;
```

The `observations` view provides a flat interface over the normalized schema. For direct table access, query `station_snapshots`, `dock_snapshots`, `bike_snapshots`, `stations`, `docks`, and `bikes`.

Parquet snapshots are also available from Cloudflare R2 as a fallback data source.

## Repository layout

```
packages/
  db/              SQL-only schema package (DuckDB migrations, seed data)
  scraper/         Python data collection pipeline (Pydantic, httpx, DuckDB)
  simulation/      Bayesian generative simulation (optional, numpy/scipy)
  website/         SvelteKit 2 dashboard (Observable Plot, MapLibre GL, Paraglide)
```

| Path | Purpose |
|------|---------|
| `packages/db/` | Normalized 7-table DuckDB schema -- the integration contract |
| `packages/scraper/` | Fetches GIRA API, validates, transforms, writes to storage |
| `packages/website/` | Public-facing data dashboard and editorial pages |
| `packages/simulation/` | Synthetic data generation for prior predictive checks |
| `.github/workflows/` | CI/CD pipelines and fallback scraper |
| `spec/` | Planning artifacts (VISION, SPEC, PLAN) |
| `METHODOLOGY.md` | Pre-registered metric definitions |

## Pre-registered metrics

All metrics are defined in [`METHODOLOGY.md`](METHODOLOGY.md) and committed before collection begins.

| Metric | What it measures |
|--------|-----------------|
| Dock Empty Rate | % of snapshots where a station has zero available bikes |
| System-Wide Availability | Available bikes as a fraction of total capacity, system-wide |
| Peak-Hour Desert Index | Empty rate during morning/evening commute windows specifically |
| Dead Dock Detector | Stations with a suspiciously constant non-zero bike count (>4 h) |
| Dock Functional Rate | Docks in unknown/broken state as a fraction of total capacity |

## Project planning

| Document | Purpose |
|----------|---------|
| [`spec/VISION.md`](spec/VISION.md) | Problem statement, target users, success criteria |
| [`spec/SPEC.md`](spec/SPEC.md) | Domain model, system architecture, data contracts |
| [`spec/PLAN.md`](spec/PLAN.md) | Milestones, task table, dependency graph |
| [`IDEA.md`](IDEA.md) | Original concept document with full rationale and ADRs |

## Transparency

This project applies three principles without exception:

- **Radical transparency** -- every line of code, every deployment config, and every raw data point is public
- **Methodological integrity** -- metrics are defined and committed before any data exists
- **Reproducibility** -- any person can clone this repository and independently reproduce every finding

See [`LEGAL.md`](LEGAL.md) for the full legal and ethical analysis, including discussion of authenticated API endpoints.

## License

[MIT](LICENSE)

---

*Open project. Contributions, scrutiny, and independent reproduction are welcome.*
