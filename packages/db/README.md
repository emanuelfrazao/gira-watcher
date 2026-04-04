# Database Schema Package

SQL-only package defining the DuckDB schema contract for GIRA Watch. All other packages (scraper, website) code against these table definitions.

## Entity-Relationship Overview

```
stations (dim)          docks (dim)              bikes (dim)
    |                       |                        |
    |  1:N                  |  1:N                   |  1:N
    v                       v                        v
station_snapshots       dock_snapshots           bike_snapshots
    |                       |                        |
    |  N:1                  |  N:1                   |  N:1
    +--------> scrape_runs <--------+--------<-------+
                  (audit)
```

**Views:**
- `observations` -- backward-compatible flat view joining station_snapshots + stations + scrape_runs
- `dead_dock_flags` -- flags stations with constant non-zero bike count for >4 consecutive hours

## Table-to-Statistics Mapping

| Table | Statistics Powered |
|-------|-------------------|
| `station_snapshots` + `stations` | Dock Empty Rate, System-Wide Availability, Peak-Hour Desert Index, Dead Dock Detector, Dock Functional Rate |
| `station_snapshots` | DTMC (consecutive bike transitions), NHPP (arrival/departure rates) |
| `dock_snapshots` | HMM (binary dock state sequences), Dead Dock precision analysis |
| `bike_snapshots` | Bike movement tracking, battery analysis, fleet health |
| `scrape_runs` | Audit trail -- every data point traced to commit + GitHub Actions run |

## GIRA API to DB Field Mapping

### getStations -> stations (dim) + station_snapshots (fact)

| API Field | Dim Column | Fact Column | Transform |
|-----------|-----------|-------------|-----------|
| `code` | `station_code` | `station_code` | direct |
| `serialNumber` | `serial_number` | -- | direct |
| `name` | `name` | -- | direct |
| `description` | `description` | -- | direct |
| `latitude` | `latitude` | -- | direct |
| `longitude` | `longitude` | -- | direct |
| `stype` | `stype` | -- | cast to enum |
| `zone` | `zone` | -- | direct |
| `creationDate` | `creation_date` | -- | parse ISO 8601 |
| `bikes` | -- | `bikes` | int |
| `docks` | -- | `docks` | int |
| `assetStatus` | -- | `asset_status` | cast to enum |
| `version` | -- | `version` | int |
| `updateDate` | -- | `update_date` | parse ISO 8601 |
| -- | `total_docks` | -- | from static public data (EMEL/GBFS), pre-populated |

### getDocks -> docks (dim) + dock_snapshots (fact)

| API Field | Dim Column | Fact Column | Transform |
|-----------|-----------|-------------|-----------|
| `code` | `dock_code` | `dock_code` | direct |
| `serialNumber` | `serial_number` | -- | direct |
| `name` | `dock_number` | -- | parse int |
| `ledStatus` | -- | `state` | `'green'` -> `'empty'`, `'red'` -> `'occupied'` |
| `lockStatus` | -- | -- | omitted: 1:1 correlated with ledStatus |
| -- | `station_code` | -- | parent station context |
| -- | -- | `bike_code` | matched bike.parent, NULL if empty |

### getBikes -> bikes (dim) + bike_snapshots (fact)

| API Field | Dim Column | Fact Column | Transform |
|-----------|-----------|-------------|-----------|
| `code` | `bike_code` | `bike_code` | direct |
| `serialNumber` | `serial_number` | -- | direct |
| `name` | `name` | -- | direct |
| `type` | `bike_type` | -- | cast to enum, nullable |
| `parent` | -- | `dock_code` | direct (dock code) |
| `battery` | -- | `battery` | parse int from string, nullable |
| -- | -- | `station_code` | parent station context |

## Column Reference

### stations

| Column | DuckDB | Python | TypeScript |
|--------|--------|--------|------------|
| `station_code` | `VARCHAR(10)` | `str` | `string` |
| `serial_number` | `VARCHAR(10)` | `str` | `string` |
| `name` | `VARCHAR` | `str` | `string` |
| `description` | `VARCHAR` | `str \| None` | `string \| null` |
| `latitude` | `DOUBLE` | `float` | `number` |
| `longitude` | `DOUBLE` | `float` | `number` |
| `stype` | `station_type ENUM` | `Literal['A', 'B']` | `'A' \| 'B'` |
| `zone` | `VARCHAR(10)` | `str \| None` | `string \| null` |
| `creation_date` | `TIMESTAMPTZ` | `datetime \| None` | `string \| null` |
| `total_docks` | `SMALLINT` | `int` | `number` |

### docks

| Column | DuckDB | Python | TypeScript |
|--------|--------|--------|------------|
| `dock_code` | `VARCHAR(10)` | `str` | `string` |
| `serial_number` | `VARCHAR(15)` | `str` | `string` |
| `station_code` | `VARCHAR(10)` | `str` | `string` |
| `dock_number` | `SMALLINT` | `int` | `number` |

### bikes

| Column | DuckDB | Python | TypeScript |
|--------|--------|--------|------------|
| `bike_code` | `VARCHAR(10)` | `str` | `string` |
| `serial_number` | `VARCHAR(10)` | `str` | `string` |
| `name` | `VARCHAR` | `str` | `string` |
| `bike_type` | `bike_type ENUM` | `Literal['electric', 'conventional'] \| None` | `'electric' \| 'conventional' \| null` |

### scrape_runs

| Column | DuckDB | Python | TypeScript |
|--------|--------|--------|------------|
| `run_id` | `VARCHAR` | `str` | `string` |
| `run_type` | `run_type ENUM` | `Literal['station', 'detail']` | `'station' \| 'detail'` |
| `commit_sha` | `VARCHAR` | `str` | `string` |
| `github_run_url` | `VARCHAR` | `str \| None` | `string \| null` |
| `started_at` | `TIMESTAMPTZ` | `datetime` | `string` |
| `finished_at` | `TIMESTAMPTZ` | `datetime \| None` | `string \| null` |
| `stations_queried` | `SMALLINT` | `int \| None` | `number \| null` |
| `docks_queried` | `INTEGER` | `int \| None` | `number \| null` |
| `bikes_queried` | `SMALLINT` | `int \| None` | `number \| null` |
| `records_written` | `INTEGER` | `int \| None` | `number \| null` |
| `exit_status` | `exit_status ENUM` | `Literal['success', 'partial', 'error']` | `'success' \| 'partial' \| 'error'` |

### station_snapshots

| Column | DuckDB | Python | TypeScript |
|--------|--------|--------|------------|
| `station_code` | `VARCHAR(10)` | `str` | `string` |
| `observed_at` | `TIMESTAMPTZ` | `datetime` | `string` |
| `run_id` | `VARCHAR` | `str` | `string` |
| `bikes` | `SMALLINT` | `int` | `number` |
| `docks` | `SMALLINT` | `int` | `number` |
| `asset_status` | `station_status ENUM` | `Literal['active', 'repair']` | `'active' \| 'repair'` |
| `version` | `INTEGER` | `int` | `number` |
| `update_date` | `TIMESTAMPTZ` | `datetime` | `string` |

### dock_snapshots

| Column | DuckDB | Python | TypeScript |
|--------|--------|--------|------------|
| `dock_code` | `VARCHAR(10)` | `str` | `string` |
| `observed_at` | `TIMESTAMPTZ` | `datetime` | `string` |
| `run_id` | `VARCHAR` | `str` | `string` |
| `state` | `dock_state ENUM` | `Literal['empty', 'occupied']` | `'empty' \| 'occupied'` |
| `bike_code` | `VARCHAR(10)` | `str \| None` | `string \| null` |

### bike_snapshots

| Column | DuckDB | Python | TypeScript |
|--------|--------|--------|------------|
| `bike_code` | `VARCHAR(10)` | `str` | `string` |
| `observed_at` | `TIMESTAMPTZ` | `datetime` | `string` |
| `run_id` | `VARCHAR` | `str` | `string` |
| `dock_code` | `VARCHAR(10)` | `str` | `string` |
| `station_code` | `VARCHAR(10)` | `str` | `string` |
| `battery` | `SMALLINT` | `int \| None` | `number \| null` |

## Development

### Prerequisites

- [DuckDB CLI](https://duckdb.org/docs/installation/) (for local development)
- [just](https://github.com/casey/just) (task runner)
- [SQLFluff](https://sqlfluff.com/) (optional, for SQL linting: `uv tool install sqlfluff`)

### Apply schema locally

```bash
cd packages/db
just apply          # Apply all migrations to gira_local.duckdb
just seed           # Apply migrations + load test fixtures
just reset          # Drop and recreate from scratch
```

Override the database file:

```bash
DB_FILE=my_test.duckdb just apply
```

### Validate SQL

```bash
just check          # Apply to :memory: DuckDB (type checking)
just lint           # SQLFluff style checking
just validate       # Both lint + check
```

### Query the seeded database

```bash
just seed
duckdb gira_local.duckdb "SELECT * FROM dead_dock_flags"
duckdb gira_local.duckdb "SELECT * FROM observations LIMIT 10"
```

## How Other Packages Consume the Schema

- **Scraper** (`packages/scraper/`): Applies migration files on startup. Defines Python `TypedDict`s matching these table columns for INSERT operations.
- **Website** (`packages/website/`): Defines TypeScript interfaces matching query result shapes. Connects to the public read-only MotherDuck share.

There are no cross-package Python/TypeScript imports. The SQL files in this package ARE the contract. Correctness is verified by integration tests that apply migrations, insert typed rows, and assert results.

## Status

Schema is **complete** -- all 7 tables (3 dimension, 3 fact, 1 audit), 2 views (observations, dead_dock_flags), enums, indexes, and test fixtures are defined and passing validation.
