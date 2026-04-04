-- Backward-compatible view: maps normalized schema to the original flat observations shape.
-- bikes_mech and bikes_elec are NULL: station-level polling cannot distinguish bike types --
-- that requires per-bike detail queries (getBikes endpoint).

CREATE OR REPLACE VIEW observations AS
SELECT
    hash(ss.station_code || ss.observed_at::VARCHAR) AS id,
    s.serial_number AS station_id,
    s.name AS station_name,
    s.latitude AS lat,
    s.longitude AS lon,
    s.total_docks,
    NULL::INTEGER AS bikes_mech,
    NULL::INTEGER AS bikes_elec,
    ss.docks AS empty_docks,
    ss.observed_at AS queried_at,
    ss.run_id,
    sr.commit_sha
FROM station_snapshots AS ss
JOIN stations AS s ON ss.station_code = s.station_code
JOIN scrape_runs AS sr ON ss.run_id = sr.run_id;
