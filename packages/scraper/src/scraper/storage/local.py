"""Local DuckDB file storage backend."""

from collections.abc import Sequence

from scraper.domain.models import (
    BikeDim,
    BikeSnapshot,
    DockDim,
    DockSnapshot,
    RunManifest,
    StationDim,
    StationSnapshot,
    WriteResult,
)


class LocalWriter:
    """Write-side interface for a single scrape run against a local DuckDB file."""

    def __init__(self, db_path: str, manifest: RunManifest) -> None:
        self._db_path = db_path
        self._manifest = manifest

    def __enter__(self) -> "LocalWriter":
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        raise NotImplementedError

    def upsert_stations(self, stations: Sequence[StationDim]) -> None:
        raise NotImplementedError

    def upsert_docks(self, docks: Sequence[DockDim]) -> None:
        raise NotImplementedError

    def upsert_bikes(self, bikes: Sequence[BikeDim]) -> None:
        raise NotImplementedError

    def write_station_snapshots(self, snapshots: Sequence[StationSnapshot]) -> None:
        raise NotImplementedError

    def write_dock_snapshots(self, snapshots: Sequence[DockSnapshot]) -> None:
        raise NotImplementedError

    def write_bike_snapshots(self, snapshots: Sequence[BikeSnapshot]) -> None:
        raise NotImplementedError

    def result(self) -> WriteResult:
        raise NotImplementedError


class LocalBackend:
    """Local DuckDB file storage backend."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def health_check(self) -> None:
        raise NotImplementedError

    def run(self, manifest: RunManifest) -> LocalWriter:
        raise NotImplementedError
