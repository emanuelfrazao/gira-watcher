"""Group 3: Domain models -- dataclass instantiation."""

from datetime import UTC, datetime

from scraper.domain.enums import (
    BikeType,
    DockState,
    ExitStatus,
    RunType,
    StationStatus,
    StationType,
)
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


def test_station_dim_instantiation() -> None:
    """3.1: StationDim constructs with all required fields."""
    dim = StationDim(
        station_code="A001",
        serial_number="SN00101",
        name="Av. Duque de Avila",
        description="Junto ao metro Saldanha",
        latitude=38.7335,
        longitude=-9.1459,
        stype=StationType.A,
        zone="zone-1",
        creation_date=datetime(2018, 6, 28, 10, 0, 0, tzinfo=UTC),
        total_docks=16,
    )
    assert dim.station_code == "A001"
    assert dim.stype == StationType.A


def test_dock_dim_instantiation() -> None:
    """3.2: DockDim constructs with all required fields."""
    dim = DockDim(
        dock_code="D001-01",
        serial_number="DSN001-01-0001",
        station_code="A001",
        dock_number=1,
    )
    assert dim.dock_code == "D001-01"


def test_bike_dim_instantiation() -> None:
    """3.3: BikeDim constructs with all required fields."""
    dim = BikeDim(
        bike_code="E001",
        serial_number="BSN00101",
        name="GIRA E001",
        bike_type=BikeType.ELECTRIC,
    )
    assert dim.bike_code == "E001"


def test_station_snapshot_instantiation() -> None:
    """3.4: StationSnapshot constructs with all required fields."""
    snap = StationSnapshot(
        station_code="A001",
        observed_at=datetime.now(UTC),
        run_id="run-001",
        bikes=5,
        docks=11,
        asset_status=StationStatus.ACTIVE,
        version=1,
        update_date=datetime.now(UTC),
    )
    assert snap.station_code == "A001"
    assert snap.bikes == 5


def test_dock_snapshot_instantiation() -> None:
    """3.5: DockSnapshot constructs with all required fields."""
    snap = DockSnapshot(
        dock_code="D001-01",
        observed_at=datetime.now(UTC),
        run_id="run-001",
        state=DockState.OCCUPIED,
        bike_code="E001",
    )
    assert snap.state == DockState.OCCUPIED


def test_bike_snapshot_instantiation() -> None:
    """3.6: BikeSnapshot constructs with all required fields."""
    snap = BikeSnapshot(
        bike_code="E001",
        observed_at=datetime.now(UTC),
        run_id="run-001",
        dock_code="D001-01",
        station_code="A001",
        battery=85,
    )
    assert snap.battery == 85


def test_run_manifest_instantiation() -> None:
    """3.7: RunManifest constructs with required fields."""
    manifest = RunManifest(
        run_id="run-001",
        run_type=RunType.STATION,
        commit_sha="abc1234",
        github_run_url=None,
        started_at=datetime.now(UTC),
        scheduler_identity="local-dev",
    )
    assert manifest.run_type == RunType.STATION


def test_write_result_instantiation() -> None:
    """3.8: WriteResult constructs with count fields."""
    result = WriteResult(
        stations_queried=3,
        docks_queried=None,
        bikes_queried=None,
        records_written=720,
        exit_status=ExitStatus.SUCCESS,
        finished_at=datetime.now(UTC),
    )
    assert result.records_written == 720
