"""Domain dataclasses mapping to DuckDB tables defined in 001_initial_schema.sql."""

import dataclasses
from datetime import datetime

from scraper.domain.enums import (
    BikeType,
    DockState,
    ExitStatus,
    RunType,
    StationStatus,
    StationType,
)

# --- Dimension dataclasses ---


@dataclasses.dataclass(frozen=True)
class StationDim:
    """Station dimension record. Maps to SQL `stations` table.

    Note: `total_docks` comes from static public data, not the GIRA API.
    """

    station_code: str
    serial_number: str
    name: str
    description: str | None
    latitude: float
    longitude: float
    stype: StationType
    zone: str | None
    creation_date: datetime | None
    total_docks: int


@dataclasses.dataclass(frozen=True)
class DockDim:
    """Dock dimension record. Maps to SQL `docks` table."""

    dock_code: str
    serial_number: str
    station_code: str
    dock_number: int


@dataclasses.dataclass(frozen=True)
class BikeDim:
    """Bike dimension record. Maps to SQL `bikes` table."""

    bike_code: str
    serial_number: str
    name: str
    bike_type: BikeType | None


# --- Fact dataclasses ---


@dataclasses.dataclass(frozen=True)
class StationSnapshot:
    """Station point-in-time observation. Maps to SQL `station_snapshots`."""

    station_code: str
    observed_at: datetime
    run_id: str
    bikes: int
    docks: int
    asset_status: StationStatus
    version: int
    update_date: datetime


@dataclasses.dataclass(frozen=True)
class DockSnapshot:
    """Dock point-in-time observation. Maps to SQL `dock_snapshots`."""

    dock_code: str
    observed_at: datetime
    run_id: str
    state: DockState
    bike_code: str | None


@dataclasses.dataclass(frozen=True)
class BikeSnapshot:
    """Bike point-in-time observation. Maps to SQL `bike_snapshots`."""

    bike_code: str
    observed_at: datetime
    run_id: str
    dock_code: str
    station_code: str
    battery: int | None


# --- Run lifecycle ---


@dataclasses.dataclass(frozen=True)
class RunManifest:
    """Metadata for a scrape run, created before the run starts.

    `scheduler_identity` is for audit dispatch and logging only -- not persisted to scrape_runs.
    """

    run_id: str
    run_type: RunType
    commit_sha: str
    github_run_url: str | None
    started_at: datetime
    scheduler_identity: str


@dataclasses.dataclass(frozen=True)
class WriteResult:
    """Aggregated write counts from a completed run."""

    stations_queried: int | None
    docks_queried: int | None
    bikes_queried: int | None
    records_written: int
    exit_status: ExitStatus
    finished_at: datetime
