"""API-to-domain model transformation functions."""

from collections.abc import Sequence
from datetime import datetime

from scraper.api.schema import ApiBike, ApiDock, ApiStation
from scraper.domain.models import (
    BikeDim,
    BikeSnapshot,
    DockDim,
    DockSnapshot,
    StationDim,
    StationSnapshot,
)


def extract_station_dims(stations: Sequence[ApiStation]) -> list[StationDim]:
    """Extract station dimension records from API station responses."""
    raise NotImplementedError


def extract_station_snapshots(
    stations: Sequence[ApiStation],
    observed_at: datetime,
    run_id: str,
) -> list[StationSnapshot]:
    """Extract station snapshot records from API station responses."""
    raise NotImplementedError


def extract_dock_dims(docks: Sequence[ApiDock], station_code: str) -> list[DockDim]:
    """Extract dock dimension records from API dock responses."""
    raise NotImplementedError


def extract_dock_snapshots(
    docks: Sequence[ApiDock],
    bikes: Sequence[ApiBike],
    observed_at: datetime,
    run_id: str,
) -> list[DockSnapshot]:
    """Extract dock snapshot records from API dock and bike responses."""
    raise NotImplementedError


def extract_bike_dims(bikes: Sequence[ApiBike]) -> list[BikeDim]:
    """Extract bike dimension records from API bike responses."""
    raise NotImplementedError


def extract_bike_snapshots(
    bikes: Sequence[ApiBike],
    station_code: str,
    observed_at: datetime,
    run_id: str,
) -> list[BikeSnapshot]:
    """Extract bike snapshot records from API bike responses."""
    raise NotImplementedError
