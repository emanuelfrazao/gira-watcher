"""TypedDicts for DuckDB INSERT row shapes. Field names match SQL column names exactly."""

from typing import TypedDict


class StationRow(TypedDict):
    station_code: str
    serial_number: str
    name: str
    description: str | None
    latitude: float
    longitude: float
    stype: str
    zone: str | None
    creation_date: str | None
    total_docks: int


class DockRow(TypedDict):
    dock_code: str
    serial_number: str
    station_code: str
    dock_number: int


class BikeRow(TypedDict):
    bike_code: str
    serial_number: str
    name: str
    bike_type: str | None


class StationSnapshotRow(TypedDict):
    station_code: str
    observed_at: str
    run_id: str
    bikes: int
    docks: int
    asset_status: str
    version: int
    update_date: str


class DockSnapshotRow(TypedDict):
    dock_code: str
    observed_at: str
    run_id: str
    state: str
    bike_code: str | None


class BikeSnapshotRow(TypedDict):
    bike_code: str
    observed_at: str
    run_id: str
    dock_code: str
    station_code: str
    battery: int | None


class ScrapeRunRow(TypedDict):
    run_id: str
    run_type: str
    commit_sha: str
    github_run_url: str | None
    started_at: str
    finished_at: str | None
    stations_queried: int | None
    docks_queried: int | None
    bikes_queried: int | None
    records_written: int | None
    exit_status: str
