# GIRA Watch

Transparent public accountability for Lisbon's shared bicycle system.

GIRA Watch collects, stores, and analyses real-time availability data from the GIRA municipal bicycle network, using only the same public API that GIRA's own mobile app uses. Every line of code, every deployment step, and every raw data point is public and reproducible.

## What this project does

GIRA operates under a public concession in Lisbon. Residents widely report persistent station emptiness and bikes that cannot be released — but no systematic evidence exists to confirm or refute this. GIRA Watch produces that evidence: a continuous, 5-minute-resolution time-series of station availability across all ~200 docking stations, analysed against five pre-registered metrics.

The methodology is committed to this repository before any data collection begins, so the findings cannot be cherry-picked after the fact.

## How it works

A GitHub Actions scheduled workflow runs every 5 minutes. It fetches all station states from the GIRA public API and appends one row per station to a MotherDuck (DuckDB) database. A Streamlit dashboard reads from that database and renders the five pre-registered metrics live. The raw database is publicly accessible — anyone can attach it in their own DuckDB instance and run arbitrary SQL.

```
GIRA public API
  → scraper/main.py  (GitHub Actions, every 5 min)
  → MotherDuck       (public ATTACH share)
  → dashboard/       (Streamlit Community Cloud)
  → analysis/        (Jupyter notebooks, findings report)
```

Every scrape run is logged with its commit SHA and GitHub Actions run URL, creating a public, auditable chain of custody from source code to stored data.

## Accessing the data

The full dataset is publicly queryable. Attach it directly in any DuckDB shell:

```sql
-- Share URL will be published here once collection is live
ATTACH '...' AS gira (READ_ONLY);
SELECT * FROM gira.observations LIMIT 10;
```

## Repository layout

| Path | Purpose |
|------|---------|
| `.github/workflows/scrape.yml` | Cron schedule — the public deployment definition |
| `scraper/main.py` | Fetches GIRA API, validates, writes to MotherDuck |
| `scraper/schema.py` | Response schema and field definitions |
| `dashboard/app.py` | Streamlit metrics dashboard |
| `dashboard/queries.py` | All SQL queries used in the dashboard |
| `analysis/notebooks/` | Jupyter notebooks for the findings report |
| `METHODOLOGY.md` | Pre-registered metric definitions |

## Pre-registered metrics

All metrics are defined in [`METHODOLOGY.md`](METHODOLOGY.md) and committed before collection begins.

| Metric | What it measures |
|--------|-----------------|
| Dock Empty Rate | % of observations where a station has zero available bikes |
| System-Wide Availability | Available bikes as a fraction of total capacity, system-wide |
| Peak-Hour Desert Index | Empty rate during morning/evening commute windows specifically |
| Dead Dock Detector | Stations with a suspiciously constant non-zero bike count (>4 h) |
| Dock Functional Rate | Docks in unknown/broken state as a fraction of total capacity |

## Project planning

| Document | Purpose |
|----------|---------|
| [`spec/VISION.md`](spec/VISION.md) | Problem statement, target users, success criteria |
| [`spec/SPEC.md`](spec/SPEC.md) | Domain model, system architecture, data contracts |
| [`spec/PLAN.md`](spec/PLAN.md) | Milestones, task table, dependency graph, risk register |
| [`IDEA.md`](IDEA.md) | Original concept document with full rationale and ADRs |

## Transparency

This project applies three principles without exception:

- **Radical transparency** — every line of code, every deployment config, and every raw data point is public
- **Methodological integrity** — metrics are defined and committed before any data exists
- **Reproducibility** — any person can clone this repository and independently reproduce every finding

GIRA Watch does not use any private or authenticated endpoint. It queries the same public API used by GIRA's own mobile application and by third-party apps such as GIRA+. No user data is collected.

## Legal note

Querying a public, unauthenticated API is not hacking and is standard practice in data journalism. This project makes no attempt to access any authenticated endpoint, internal system, or administrative interface. See [`IDEA.md § 5`](IDEA.md) for the full legal and ethical analysis.

---

*Open project. Contributions, scrutiny, and independent reproduction are welcome.*
