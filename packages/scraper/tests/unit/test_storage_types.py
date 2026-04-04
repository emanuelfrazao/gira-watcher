"""Group 7: Storage TypedDicts -- key alignment with SQL column names."""

from typing import get_type_hints

import pytest

from scraper.domain.typed_dicts import (
    BikeRow,
    BikeSnapshotRow,
    DockRow,
    DockSnapshotRow,
    ScrapeRunRow,
    StationRow,
    StationSnapshotRow,
)


@pytest.mark.parametrize(
    ("typed_dict_class", "expected_keys"),
    [
        (
            StationRow,
            {
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
            },
        ),
        (
            DockRow,
            {"dock_code", "serial_number", "station_code", "dock_number"},
        ),
        (
            BikeRow,
            {"bike_code", "serial_number", "name", "bike_type"},
        ),
        (
            StationSnapshotRow,
            {
                "station_code",
                "observed_at",
                "run_id",
                "bikes",
                "docks",
                "asset_status",
                "version",
                "update_date",
            },
        ),
        (
            DockSnapshotRow,
            {"dock_code", "observed_at", "run_id", "state", "bike_code"},
        ),
        (
            BikeSnapshotRow,
            {"bike_code", "observed_at", "run_id", "dock_code", "station_code", "battery"},
        ),
        (
            ScrapeRunRow,
            {
                "run_id",
                "run_type",
                "commit_sha",
                "github_run_url",
                "started_at",
                "finished_at",
                "stations_queried",
                "docks_queried",
                "bikes_queried",
                "records_written",
                "exit_status",
            },
        ),
    ],
    ids=[
        "StationRow",
        "DockRow",
        "BikeRow",
        "StationSnapshotRow",
        "DockSnapshotRow",
        "BikeSnapshotRow",
        "ScrapeRunRow",
    ],
)
def test_typed_dict_keys_match_sql_columns(
    typed_dict_class: type[object],
    expected_keys: set[str],
) -> None:
    """7.1-7.7: TypedDict keys exactly match the corresponding SQL table columns."""
    actual_keys = set(get_type_hints(typed_dict_class).keys())
    assert actual_keys == expected_keys
