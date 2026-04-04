"""Group 5: Pydantic API schema -- validation tests."""

from typing import Any

import pytest
from pydantic import ValidationError

from scraper.api.schema import ApiBike, ApiDock, ApiStation


def test_api_station_validates_sample_json(sample_station_json: dict[str, Any]) -> None:
    """5.1: ApiStation parses a representative station object."""
    station = ApiStation.model_validate(sample_station_json)
    assert station.code == "A001"
    assert station.serial_number == "SN00101"
    assert station.name == "Av. Duque de Avila"
    assert station.latitude == 38.7335
    assert station.bikes == 5
    assert station.asset_status == "active"


def test_api_dock_validates_sample_json(sample_dock_json: dict[str, Any]) -> None:
    """5.2: ApiDock parses a representative dock object."""
    dock = ApiDock.model_validate(sample_dock_json)
    assert dock.code == "D001-01"
    assert dock.serial_number == "DSN001-01-0001"
    assert dock.led_status == "green"


def test_api_bike_validates_sample_json(sample_bike_json: dict[str, Any]) -> None:
    """5.3: ApiBike parses a representative bike object."""
    bike = ApiBike.model_validate(sample_bike_json)
    assert bike.code == "E001"
    assert bike.battery == "85"
    assert bike.bike_type == "electric"
    assert bike.parent == "D001-01"


def test_missing_required_field_raises_validation_error(
    sample_station_json: dict[str, Any],
) -> None:
    """5.4: Missing required field raises ValidationError."""
    incomplete = {k: v for k, v in sample_station_json.items() if k != "code"}
    with pytest.raises(ValidationError):
        ApiStation.model_validate(incomplete)


def test_extra_unknown_fields_are_tolerated(sample_station_json: dict[str, Any]) -> None:
    """5.5: Extra unknown fields don't cause validation errors."""
    extended = {**sample_station_json, "unknownField": "surprise"}
    station = ApiStation.model_validate(extended)
    assert station.code == "A001"


def test_wrong_type_for_numeric_field_raises_validation_error(
    sample_station_json: dict[str, Any],
) -> None:
    """5.6: Wrong type for numeric field raises ValidationError."""
    bad_data = {**sample_station_json, "bikes": "not_a_number"}
    with pytest.raises(ValidationError):
        ApiStation.model_validate(bad_data)
