"""MotherDuck storage backend."""

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


class MotherDuckWriter:
    """Write-side interface for a single scrape run against MotherDuck."""

    def __init__(self, connection_url: str, token: str, manifest: RunManifest) -> None:
        self._connection_url = connection_url
        self._token = token
        self._manifest = manifest

    def __enter__(self) -> "MotherDuckWriter":
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


class MotherDuckBackend:
    """MotherDuck (cloud DuckDB) storage backend."""

    def __init__(self, connection_url: str, token: str) -> None:
        self._connection_url = connection_url
        self._token = token

    def health_check(self) -> None:
        raise NotImplementedError

    def run(self, manifest: RunManifest) -> MotherDuckWriter:
        raise NotImplementedError
