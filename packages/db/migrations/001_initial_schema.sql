-- GIRA Watch: Core schema
-- Optimized for DuckDB columnar aggregation of time-series station/dock/bike snapshots.
-- No explicit indexes beyond composite PKs -- DuckDB zonemaps on chronologically-appended
-- data handle time-range pruning automatically.

-- === Enum Types ===

CREATE TYPE IF NOT EXISTS station_status AS ENUM ('active', 'repair');
CREATE TYPE IF NOT EXISTS station_type AS ENUM ('A', 'B');
CREATE TYPE IF NOT EXISTS dock_state AS ENUM ('empty', 'occupied');
CREATE TYPE IF NOT EXISTS bike_type AS ENUM ('electric', 'conventional');
CREATE TYPE IF NOT EXISTS run_type AS ENUM ('station', 'detail');
CREATE TYPE IF NOT EXISTS exit_status AS ENUM ('success', 'partial', 'error');

-- === Dimension Tables ===

CREATE TABLE IF NOT EXISTS stations (
    station_code    VARCHAR(10) PRIMARY KEY,
    serial_number   VARCHAR(10) NOT NULL,
    name            VARCHAR NOT NULL,
    description     VARCHAR,
    latitude        DOUBLE NOT NULL,
    longitude       DOUBLE NOT NULL,
    stype           station_type NOT NULL,
    zone            VARCHAR(10),
    creation_date   TIMESTAMPTZ,
    total_docks     SMALLINT NOT NULL
    -- first_seen/last_seen: derive from MIN/MAX(observed_at) on station_snapshots
);

CREATE TABLE IF NOT EXISTS docks (
    dock_code       VARCHAR(10) PRIMARY KEY,
    serial_number   VARCHAR(15) NOT NULL,
    station_code    VARCHAR(10) NOT NULL REFERENCES stations(station_code),
    dock_number     SMALLINT NOT NULL
    -- first_seen/last_seen: derive from MIN/MAX(observed_at) on dock_snapshots
);

CREATE TABLE IF NOT EXISTS bikes (
    bike_code       VARCHAR(10) PRIMARY KEY,
    serial_number   VARCHAR(10) NOT NULL,
    name            VARCHAR NOT NULL,
    bike_type       bike_type
    -- first_seen/last_seen: derive from MIN/MAX(observed_at) on bike_snapshots
);

-- === Audit Table ===

CREATE TABLE IF NOT EXISTS scrape_runs (
    run_id          VARCHAR PRIMARY KEY,
    run_type        run_type NOT NULL,
    commit_sha      VARCHAR NOT NULL,
    github_run_url  VARCHAR,
    started_at      TIMESTAMPTZ NOT NULL,
    finished_at     TIMESTAMPTZ,
    stations_queried SMALLINT,
    docks_queried   INTEGER,
    bikes_queried   SMALLINT,
    records_written INTEGER,
    exit_status     exit_status NOT NULL
);

-- === Fact Tables ===

-- Powers: Dock Empty Rate, System-Wide Availability, Peak-Hour Desert Index,
--         Dead Dock Detector, Dock Functional Rate, DTMC, NHPP.
CREATE TABLE IF NOT EXISTS station_snapshots (
    station_code    VARCHAR(10) NOT NULL REFERENCES stations(station_code),
    observed_at     TIMESTAMPTZ NOT NULL,
    run_id          VARCHAR NOT NULL REFERENCES scrape_runs(run_id),
    bikes           SMALLINT NOT NULL,
    docks           SMALLINT NOT NULL,
    asset_status    station_status NOT NULL,
    version         INTEGER NOT NULL,
    update_date     TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (station_code, observed_at)
);

-- Powers: HMM dock state detection, Dead Dock precision analysis.
CREATE TABLE IF NOT EXISTS dock_snapshots (
    dock_code       VARCHAR(10) NOT NULL REFERENCES docks(dock_code),
    observed_at     TIMESTAMPTZ NOT NULL,
    run_id          VARCHAR NOT NULL REFERENCES scrape_runs(run_id),
    state           dock_state NOT NULL,
    bike_code       VARCHAR(10),
    PRIMARY KEY (dock_code, observed_at)
);

-- Powers: bike movement tracking, battery analysis, fleet health.
-- dock_code and station_code have no FK constraints: denormalized for query convenience.
-- Referential integrity validated at scraper level before INSERT.
CREATE TABLE IF NOT EXISTS bike_snapshots (
    bike_code       VARCHAR(10) NOT NULL REFERENCES bikes(bike_code),
    observed_at     TIMESTAMPTZ NOT NULL,
    run_id          VARCHAR NOT NULL REFERENCES scrape_runs(run_id),
    dock_code       VARCHAR(10) NOT NULL,
    station_code    VARCHAR(10) NOT NULL,
    battery         SMALLINT,
    PRIMARY KEY (bike_code, observed_at)
);
