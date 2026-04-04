"""Group 8: In-memory DuckDB fixture -- migration application and constraints."""

import duckdb
import pytest


def test_migrations_apply_cleanly(db_connection: duckdb.DuckDBPyConnection) -> None:
    """8.1: In-memory DuckDB with migrations applied; no errors."""
    result = db_connection.execute("SELECT 1").fetchone()
    assert result is not None
    assert result[0] == 1


def test_all_expected_tables_exist(db_connection: duckdb.DuckDBPyConnection) -> None:
    """8.2: All 7 expected tables exist."""
    tables = {
        row[0]
        for row in db_connection.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        ).fetchall()
    }
    expected = {
        "stations",
        "docks",
        "bikes",
        "scrape_runs",
        "station_snapshots",
        "dock_snapshots",
        "bike_snapshots",
    }
    assert expected.issubset(tables)


def test_all_expected_enum_types_exist(db_connection: duckdb.DuckDBPyConnection) -> None:
    """8.3: All 6 expected enum types are registered."""
    types = {
        row[0]
        for row in db_connection.execute(
            "SELECT type_name FROM duckdb_types() WHERE type_category IS NULL"
        ).fetchall()
    }
    expected = {
        "station_status",
        "station_type",
        "dock_state",
        "bike_type",
        "run_type",
        "exit_status",
    }
    assert expected.issubset(types)


def test_station_table_has_correct_columns(db_connection: duckdb.DuckDBPyConnection) -> None:
    """8.4: stations table column names match DDL."""
    columns = {
        row[0]
        for row in db_connection.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'stations' AND table_schema = 'main'"
        ).fetchall()
    }
    expected = {
        "station_code",
        "serial_number",
        "name",
        "description",
        "latitude",
        "longitude",
        "stype",
        "zone",
        "creation_date",
        "total_docks",
    }
    assert columns == expected


def test_foreign_key_constraint_enforced(db_connection: duckdb.DuckDBPyConnection) -> None:
    """8.5: Insert into station_snapshots without matching station row fails."""
    db_connection.execute(
        "INSERT INTO scrape_runs (run_id, run_type, commit_sha, started_at, exit_status) "
        "VALUES ('test-run', 'station', 'abc', '2026-01-01T00:00:00Z', 'success')"
    )
    with pytest.raises(duckdb.ConstraintException):
        db_connection.execute(
            "INSERT INTO station_snapshots "
            "(station_code, observed_at, run_id, bikes, docks, asset_status, version, update_date) "
            "VALUES ('NONEXISTENT', '2026-01-01T00:00:00Z', 'test-run', 0, 0, 'active', 1, "
            "'2026-01-01T00:00:00Z')"
        )


def test_enum_constraint_enforced(db_connection: duckdb.DuckDBPyConnection) -> None:
    """8.6: Insert invalid enum value into station_snapshots fails."""
    db_connection.execute(
        "INSERT INTO stations (station_code, serial_number, name, latitude, longitude, "
        "stype, total_docks) VALUES ('TEST', 'SN999', 'Test', 38.7, -9.1, 'A', 10)"
    )
    db_connection.execute(
        "INSERT INTO scrape_runs (run_id, run_type, commit_sha, started_at, exit_status) "
        "VALUES ('test-run-2', 'station', 'abc', '2026-01-01T00:00:00Z', 'success')"
    )
    with pytest.raises(duckdb.ConversionException):
        db_connection.execute(
            "INSERT INTO station_snapshots "
            "(station_code, observed_at, run_id, bikes, docks, asset_status, version, update_date) "
            "VALUES ('TEST', '2026-01-01T00:00:00Z', 'test-run-2', 0, 0, 'invalid', 1, "
            "'2026-01-01T00:00:00Z')"
        )
