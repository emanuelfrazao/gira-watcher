"""Storage Protocol definitions for the scraper."""

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

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


@runtime_checkable
class RunWriter(Protocol):
    """Write-side interface for a single scrape run.

    Obtained from StorageBackend.run(). Synchronous context manager -- __enter__
    begins transaction, __exit__ commits/rollbacks. Dimension upserts before
    fact writes. Intentionally sync (DuckDB is synchronous).
    """

    def __enter__(self) -> "RunWriter": ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None: ...

    def upsert_stations(self, stations: Sequence[StationDim]) -> None: ...

    def upsert_docks(self, docks: Sequence[DockDim]) -> None: ...

    def upsert_bikes(self, bikes: Sequence[BikeDim]) -> None: ...

    def write_station_snapshots(self, snapshots: Sequence[StationSnapshot]) -> None: ...

    def write_dock_snapshots(self, snapshots: Sequence[DockSnapshot]) -> None: ...

    def write_bike_snapshots(self, snapshots: Sequence[BikeSnapshot]) -> None: ...

    def result(self) -> WriteResult: ...


@runtime_checkable
class StorageBackend(Protocol):
    """Top-level storage interface. Implementations: MotherDuck, Local, Parquet."""

    def health_check(self) -> None: ...

    def run(self, manifest: RunManifest) -> RunWriter: ...
