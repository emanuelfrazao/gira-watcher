"""Parquet-to-R2 storage backend."""

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


class ParquetWriter:
    """Write-side interface for a single scrape run writing Parquet files.

    Dimension methods are no-ops -- Parquet backend only writes snapshot data.
    """

    def __init__(self, output_dir: str, manifest: RunManifest) -> None:
        self._output_dir = output_dir
        self._manifest = manifest

    def __enter__(self) -> "ParquetWriter":
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        raise NotImplementedError

    def upsert_stations(self, stations: Sequence[StationDim]) -> None:
        """No-op for Parquet backend -- dimensions not written to Parquet."""

    def upsert_docks(self, docks: Sequence[DockDim]) -> None:
        """No-op for Parquet backend -- dimensions not written to Parquet."""

    def upsert_bikes(self, bikes: Sequence[BikeDim]) -> None:
        """No-op for Parquet backend -- dimensions not written to Parquet."""

    def write_station_snapshots(self, snapshots: Sequence[StationSnapshot]) -> None:
        raise NotImplementedError

    def write_dock_snapshots(self, snapshots: Sequence[DockSnapshot]) -> None:
        raise NotImplementedError

    def write_bike_snapshots(self, snapshots: Sequence[BikeSnapshot]) -> None:
        raise NotImplementedError

    def result(self) -> WriteResult:
        raise NotImplementedError


class ParquetBackend:
    """Parquet-to-R2 fallback storage backend."""

    def __init__(self, output_dir: str) -> None:
        self._output_dir = output_dir

    def health_check(self) -> None:
        raise NotImplementedError

    def run(self, manifest: RunManifest) -> ParquetWriter:
        raise NotImplementedError
