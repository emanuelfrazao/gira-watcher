# Pre-Registered Methodology

> These metrics are locked before collection begins. Changing them after data has been collected would compromise the integrity of the project and must be documented as a methodological amendment (see [Amendment Protocol](#amendment-protocol) below).

## Data Source

The GIRA mobile application communicates with an internal REST API to display real-time station status. GIRA Watch queries these endpoints at two tiers:

- **Station-level data** (`getStations`): Unauthenticated, publicly reachable -- the same endpoint used by third-party applications such as GIRA+. Returns aggregate bike/dock counts per station. This tier powers all five pre-registered metrics.
- **Dock/bike detail data** (`getDocks`, `getBikes`): Authenticated via JWT using the project maintainer's own legitimate GIRA account. Returns per-dock state and per-bike battery/position data. This tier provides supplementary granularity for the Dead Dock Detector and fleet health analysis but is not required for the core metrics.

No credentials are bypassed or misused. No user data, trip data, or personally identifiable information is collected or stored.

## Collection Parameters

- **Frequency:** every 5 minutes
- **Scheduler:** VPS primary (systemd timer, `AccuracySec=1us`) with GitHub Actions fallback (cron schedule)
- **Coverage:** all docking stations returned by the stations list endpoint (~200 stations)
- **Fields collected per station per snapshot:** station code, available bikes (aggregate count), available docks, asset status, version, update timestamp
- **Detail fields (authenticated tier):** per-dock state (empty/occupied), per-bike battery level, per-bike dock assignment
- **Minimum collection period before publication of findings:** 90 days

## Schema

Data is stored in a normalized DuckDB schema (see [`packages/db/`](packages/db/) for the full DDL):

- **Dimension tables:** `stations`, `docks`, `bikes` -- slowly-changing attributes
- **Fact tables:** `station_snapshots`, `dock_snapshots`, `bike_snapshots` -- one row per entity per scrape run
- **Audit table:** `scrape_runs` -- one row per execution with `run_id`, `commit_sha`, `github_run_url`, `exit_status`

A backward-compatible `observations` VIEW joins `station_snapshots` with `stations` and `scrape_runs`, providing a flat interface that matches the original schema design. The pre-registered metrics below reference the canonical tables (`station_snapshots` joined with `stations`), not the view.

A `dead_dock_flags` VIEW identifies stations matching the Dead Dock Detector pattern (see below).

## Pre-Registered Metrics

### Dock Empty Rate

For each station: the percentage of snapshots where `bikes = 0` (from `station_snapshots`). Reported as a daily average and a rolling 30-day average. A station is classified as *chronically unavailable* if its 30-day empty rate exceeds **70%**.

**Data source:** `station_snapshots.bikes`, keyed by `station_snapshots.station_code`.

### System-Wide Availability

At each 5-minute interval: `SUM(station_snapshots.bikes) / SUM(stations.total_docks)` across all active stations. Reported as hourly and daily averages. Decomposed by bike type where detail-tier data is available (dock/bike snapshots provide the mechanical vs electric breakdown; station-level data provides only an aggregate `bikes` count).

**Data source:** `station_snapshots.bikes`, `stations.total_docks`.

### Peak-Hour Desert Index

Morning peak defined as **07:30--09:30** local time, Monday--Friday. Evening peak defined as **17:30--19:30** local time, Monday--Friday. For each station: empty rate (`bikes = 0`) during peak hours specifically, compared to its overall empty rate. Stations with empty rate > **80%** during peaks are flagged.

**Data source:** `station_snapshots.bikes`, `station_snapshots.observed_at`.

### Dead Dock Detector

A station is flagged as potentially reporting phantom availability if its non-zero bike count remains **exactly constant for more than 4 consecutive hours**. This pattern is inconsistent with normal usage and suggests bikes are physically locked or the API is returning stale data.

Flagged snapshots are identified by the `dead_dock_flags` VIEW and **excluded from all availability metrics** (Dock Empty Rate, System-Wide Availability, Peak-Hour Desert Index, Dock Functional Rate). They are reported separately in the Dead Dock Detector panel.

**Data source:** `station_snapshots.bikes`, `station_snapshots.observed_at`, `dead_dock_flags` VIEW.

### Dock Functional Rate

For each station: `stations.total_docks - station_snapshots.bikes - station_snapshots.docks = docks in unknown/broken state`. Reported as a percentage of total capacity. A station where `broken_docks / total_docks > 50%` for more than **14 consecutive days** is classified as *structurally degraded*.

**Data source:** `station_snapshots.bikes`, `station_snapshots.docks`, `stations.total_docks`.

## Amendment Protocol

The five metrics above are pre-registered. After data collection has begun:

1. **No metric may be silently added, removed, or modified.** Any change constitutes a methodological amendment.
2. An amendment requires a **dedicated commit** with a clear rationale in the commit message (prefixed `docs(methodology):`).
3. The amendment must be noted in this section with the date, description, and justification.
4. The original metric definition is preserved (struck through or quoted) alongside the amended version for auditability.
5. Dashboard queries in `packages/website/` must be updated to match any amended definitions.

### Amendments

*None. Collection has not yet begun.*
