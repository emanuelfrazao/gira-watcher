"""Shared test fixtures: in-memory DuckDB connection, sample API JSON data."""

import pathlib
from typing import Any

import duckdb
import pytest

# --- Database fixtures ---

_MIGRATIONS_DIR = pathlib.Path(__file__).resolve().parents[2] / "db" / "migrations"


@pytest.fixture
def db_connection() -> duckdb.DuckDBPyConnection:
    """Create an in-memory DuckDB connection with all migrations applied."""
    conn = duckdb.connect(":memory:")
    migration_files = sorted(_MIGRATIONS_DIR.glob("*.sql"))
    for migration_file in migration_files:
        sql = migration_file.read_text()
        conn.execute(sql)
    yield conn  # type: ignore[misc]
    conn.close()


# --- Sample API JSON fixtures ---


@pytest.fixture(scope="session")
def sample_station_json() -> dict[str, Any]:
    """Representative GIRA API station response object."""
    return {
        "code": "A001",
        "serialNumber": "SN00101",
        "name": "Av. Duque de Avila",
        "description": "Junto ao metro Saldanha",
        "latitude": 38.7335,
        "longitude": -9.1459,
        "bikes": 5,
        "docks": 11,
        "stype": "A",
        "zone": "zone-1",
        "creationDate": "2018-06-28T10:00:00+01:00",
        "assetStatus": "active",
        "version": 1,
        "updateDate": "2026-03-15T06:00:00+00:00",
    }


@pytest.fixture(scope="session")
def sample_dock_json() -> dict[str, Any]:
    """Representative GIRA API dock response object."""
    return {
        "code": "D001-01",
        "serialNumber": "DSN001-01-0001",
        "name": "1",
        "ledStatus": "green",
    }


@pytest.fixture(scope="session")
def sample_bike_json() -> dict[str, Any]:
    """Representative GIRA API bike response object."""
    return {
        "code": "E001",
        "serialNumber": "BSN00101",
        "name": "GIRA E001",
        "battery": "85",
        "type": "electric",
        "parent": "D001-01",
    }


@pytest.fixture(scope="session")
def sample_station_response_json(sample_station_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Wraps sample station JSON in a list envelope."""
    return [sample_station_json]


@pytest.fixture(scope="session")
def sample_dock_response_json(sample_dock_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Wraps sample dock JSON in a list envelope."""
    return [sample_dock_json]


@pytest.fixture(scope="session")
def sample_bike_response_json(sample_bike_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Wraps sample bike JSON in a list envelope."""
    return [sample_bike_json]
