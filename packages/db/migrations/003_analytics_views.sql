-- Dead Dock Detector: flags station-time ranges where non-zero bike count stayed
-- constant for >4 consecutive hours. Excluded from all availability metrics per
-- METHODOLOGY.md.
--
-- Uses cumulative gap-indicator technique (robust to timing jitter):
-- A new group starts when either the bikes count changes OR the gap between
-- consecutive observations exceeds 90 seconds (tolerates ~30s jitter on 1-min cadence).
-- This avoids the ROW_NUMBER * INTERVAL trick which breaks with any timing drift.

CREATE OR REPLACE VIEW dead_dock_flags AS
WITH gaps AS (
    SELECT
        station_code,
        observed_at,
        bikes,
        CASE
            WHEN
                bikes ! = LAG(bikes) OVER (PARTITION BY station_code ORDER BY observed_at)
                OR observed_at - LAG(observed_at) OVER (
                    PARTITION BY station_code ORDER BY observed_at
                ) > INTERVAL '90 seconds'
                THEN 1
            ELSE 0
        END AS new_group
    FROM station_snapshots
    WHERE bikes > 0
),

groups AS (
    SELECT
        station_code,
        observed_at,
        bikes,
        SUM(new_group) OVER (PARTITION BY station_code ORDER BY observed_at) AS grp
    FROM gaps
)

SELECT
    station_code,
    MIN(observed_at) AS flag_start,
    MAX(observed_at) AS flag_end,
    bikes,
    EXTRACT(EPOCH FROM (MAX(observed_at) - MIN(observed_at))) / 3600.0 AS duration_hours
FROM groups
GROUP BY station_code, bikes, grp
HAVING EXTRACT(EPOCH FROM (MAX(observed_at) - MIN(observed_at))) > 4 * 3600;
