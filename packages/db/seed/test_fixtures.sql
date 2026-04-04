-- Test fixtures for GIRA Watch database schema.
-- Provides minimal but realistic seed data covering all statistical patterns.
--
-- Timeline: 2026-03-15 06:00 to 12:00 UTC (6 hours, 1-min cadence)
-- Peak-hour window: 08:00-09:00 (covered by minute 120-180)

-- === Stations ===
-- 3 stations: type A active (16 docks), type B active (10 docks), type A repair (12 docks)

INSERT INTO stations (station_code, serial_number, name, description, latitude, longitude, stype, zone, creation_date, total_docks) VALUES
('A001', 'SN00101', 'Av. Duque de Avila', 'Junto ao metro Saldanha', 38.7335, -9.1459, 'A', 'zone-1', '2018-06-28T10:00:00+01:00', 16),
('B001', 'SN00201', 'Terreiro do Paco', 'Frente ao rio', 38.7076, -9.1365, 'B', 'zone-2', '2019-03-15T09:00:00+01:00', 10),
('A002', 'SN00102', 'Parque das Nacoes', 'Junto a estacao do Oriente', 38.7680, -9.0940, 'A', 'zone-3', '2018-09-01T10:00:00+01:00', 12);

-- === Docks ===
-- 5 docks across the 2 active stations (A001 and B001)

INSERT INTO docks (dock_code, serial_number, station_code, dock_number) VALUES
('D001-01', 'DSN001-01-0001', 'A001', 1),
('D001-02', 'DSN001-02-0001', 'A001', 2),
('D001-03', 'DSN001-03-0001', 'A001', 3),
('D002-01', 'DSN002-01-0001', 'B001', 1),
('D002-02', 'DSN002-02-0001', 'B001', 2);

-- === Bikes ===
-- 3 bikes: 2 electric, 1 null-type (conventional type unknown from API)

INSERT INTO bikes (bike_code, serial_number, name, bike_type) VALUES
('E001', 'BSN00101', 'GIRA E001', 'electric'),
('E002', 'BSN00102', 'GIRA E002', 'electric'),
('C001', 'BSN00201', 'GIRA C001', NULL);

-- === Scrape Runs ===
-- 4 runs: 2 station-type, 2 detail-type, 1 with exit_status='error'
-- run_stn_1 covers the full 6-hour station snapshot window
-- run_stn_2 is a failed run (error status, no data written)
-- run_dtl_1 and run_dtl_2 cover the detail snapshots

INSERT INTO scrape_runs (
    run_id,
    run_type,
    commit_sha,
    github_run_url,
    started_at,
    finished_at,
    stations_queried,
    docks_queried,
    bikes_queried,
    records_written,
    exit_status
) VALUES
(
    'run_stn_1',
    'station',
    'abc1234',
    'https://github.com/owner/gira-watcher/actions/runs/1001',
    '2026-03-15T05:59:50+00:00',
    '2026-03-15T12:00:10+00:00',
    3,
    NULL,
    NULL,
    720,
    'success'
),
(
    'run_stn_2',
    'station',
    'abc1234',
    'https://github.com/owner/gira-watcher/actions/runs/1002',
    '2026-03-15T12:05:00+00:00',
    '2026-03-15T12:05:02+00:00',
    0,
    NULL,
    NULL,
    0,
    'error'
),
(
    'run_dtl_1',
    'detail',
    'abc1234',
    'https://github.com/owner/gira-watcher/actions/runs/1003',
    '2026-03-15T06:00:00+00:00',
    '2026-03-15T09:00:05+00:00',
    NULL,
    5,
    3,
    24,
    'success'
),
(
    'run_dtl_2',
    'detail',
    'def5678',
    'https://github.com/owner/gira-watcher/actions/runs/1004',
    '2026-03-15T09:00:00+00:00',
    '2026-03-15T12:00:05+00:00',
    NULL,
    5,
    3,
    24,
    'success'
);

-- === Station Snapshots ===
-- 6 hours x 1-min cadence x 2 stations = 720 rows
--
-- Station A001 (Dead Dock trigger):
--   Minutes 0-299 (5 hours): constant bikes=3, docks=13 (dead dock scenario)
--   Minutes 300-359 (last hour): bikes varies 1-5 (normal operation resumes)
--
-- Station B001 (fluctuating, includes empty and peak-hour):
--   Minutes 0-119 (pre-peak): bikes alternates 1-3
--   Minutes 120-179 (peak 08:00-09:00): bikes mostly 0-1 (high demand, Dock Empty Rate)
--   Minutes 180-359 (post-peak): bikes 2-3 (recovery)

INSERT INTO station_snapshots (station_code, observed_at, run_id, bikes, docks, asset_status, version, update_date)
SELECT
    'A001' AS station_code,
    TIMESTAMPTZ '2026-03-15 06:00:00+00' + (i * INTERVAL '1 minute') AS observed_at,
    'run_stn_1' AS run_id,
    CASE
        WHEN i < 300 THEN 3                    -- constant bikes=3 for 5 hours (dead dock)
        ELSE 1 + (i % 5)                       -- varies 1-5 for last hour
    END AS bikes,
    CASE
        WHEN i < 300 THEN 13                   -- 16 total - 3 bikes = 13 empty docks
        ELSE 16 - (1 + (i % 5))               -- adjusts with bikes
    END AS docks,
    'active' AS asset_status,
    1 AS version,
    TIMESTAMPTZ '2026-03-15 06:00:00+00' + (i * INTERVAL '1 minute') AS update_date
FROM generate_series(0, 359) AS t (i);

INSERT INTO station_snapshots (station_code, observed_at, run_id, bikes, docks, asset_status, version, update_date)
SELECT
    'B001' AS station_code,
    TIMESTAMPTZ '2026-03-15 06:00:00+00' + (i * INTERVAL '1 minute') AS observed_at,
    'run_stn_1' AS run_id,
    CASE
        WHEN i < 120 THEN 1 + (i % 3)         -- pre-peak: 1, 2, 3, 1, 2, 3, ...
        WHEN i < 180 THEN (i % 2)             -- peak 08:00-09:00: alternates 0 and 1
        ELSE 2 + (i % 2)                       -- post-peak: alternates 2 and 3
    END AS bikes,
    CASE
        WHEN i < 120 THEN 10 - (1 + (i % 3))  -- pre-peak
        WHEN i < 180 THEN 10 - (i % 2)        -- peak: 10 or 9
        ELSE 10 - (2 + (i % 2))               -- post-peak: 8 or 7
    END AS docks,
    'active' AS asset_status,
    1 AS version,
    TIMESTAMPTZ '2026-03-15 06:00:00+00' + (i * INTERVAL '1 minute') AS update_date
FROM generate_series(0, 359) AS t (i);

-- === Dock Snapshots ===
-- 5-min cadence subset covering state transitions (12 rows)
-- Docks on station A001: D001-01 occupied throughout, D001-02 transitions, D001-03 empty
-- Docks on station B001: D002-01 and D002-02 alternate states

INSERT INTO dock_snapshots (dock_code, observed_at, run_id, state, bike_code) VALUES
-- D001-01: occupied with E001 throughout
('D001-01', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'occupied', 'E001'),
('D001-01', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'occupied', 'E001'),
('D001-01', '2026-03-15T06:10:00+00:00', 'run_dtl_1', 'occupied', 'E001'),
-- D001-02: starts empty, becomes occupied
('D001-02', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'empty', NULL),
('D001-02', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'occupied', 'C001'),
('D001-02', '2026-03-15T06:10:00+00:00', 'run_dtl_1', 'occupied', 'C001'),
-- D001-03: empty throughout
('D001-03', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'empty', NULL),
('D001-03', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'empty', NULL),
-- D002-01: occupied then empty (bike departs)
('D002-01', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'occupied', 'E002'),
('D002-01', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'empty', NULL),
-- D002-02: empty then occupied (bike arrives)
('D002-02', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'empty', NULL),
('D002-02', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'occupied', 'E002');

-- === Bike Snapshots ===
-- 5-min cadence, one bike changes station (E002 moves A001->B001), one has null battery
-- 12 rows total

INSERT INTO bike_snapshots (bike_code, observed_at, run_id, dock_code, station_code, battery) VALUES
-- E001: stays at A001, battery decreasing
('E001', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'D001-01', 'A001', 85),
('E001', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'D001-01', 'A001', 84),
('E001', '2026-03-15T06:10:00+00:00', 'run_dtl_1', 'D001-01', 'A001', 83),
('E001', '2026-03-15T09:00:00+00:00', 'run_dtl_2', 'D001-01', 'A001', 72),
-- E002: moves from B001 to A001 (station change for movement tracking)
('E002', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'D002-01', 'B001', 90),
('E002', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'D002-02', 'B001', 89),
('E002', '2026-03-15T09:00:00+00:00', 'run_dtl_2', 'D001-02', 'A001', 78),
('E002', '2026-03-15T09:05:00+00:00', 'run_dtl_2', 'D001-02', 'A001', 77),
-- C001: conventional bike, null battery (not electric)
('C001', '2026-03-15T06:00:00+00:00', 'run_dtl_1', 'D001-02', 'A001', NULL),
('C001', '2026-03-15T06:05:00+00:00', 'run_dtl_1', 'D001-02', 'A001', NULL),
('C001', '2026-03-15T09:00:00+00:00', 'run_dtl_2', 'D001-03', 'A001', NULL),
('C001', '2026-03-15T09:05:00+00:00', 'run_dtl_2', 'D001-03', 'A001', NULL);
