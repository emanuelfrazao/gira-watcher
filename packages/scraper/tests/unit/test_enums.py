"""Group 2: Domain enums -- member alignment with SQL schema."""

import enum

import pytest

from scraper.domain.enums import (
    BikeType,
    DockState,
    ExitStatus,
    RunType,
    StationStatus,
    StationType,
)


@pytest.mark.parametrize(
    ("enum_class", "expected_values"),
    [
        (StationStatus, {"active", "repair"}),
        (StationType, {"A", "B"}),
        (DockState, {"empty", "occupied"}),
        (BikeType, {"electric", "conventional"}),
        (RunType, {"station", "detail"}),
        (ExitStatus, {"success", "partial", "error"}),
    ],
    ids=["StationStatus", "StationType", "DockState", "BikeType", "RunType", "ExitStatus"],
)
def test_enum_has_expected_members(enum_class: type[enum.Enum], expected_values: set[str]) -> None:
    """2.1-2.6: Each enum has exactly the expected values from SQL schema."""
    actual_values = {member.value for member in enum_class}
    assert actual_values == expected_values
