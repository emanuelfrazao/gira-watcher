"""Pydantic models for GIRA API response validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApiStation(BaseModel):
    """Validates a station from the getStations response. Extra fields ignored."""

    model_config = ConfigDict(extra="ignore")

    code: str
    serial_number: str = Field(alias="serialNumber")
    name: str
    description: str | None = None
    latitude: float
    longitude: float
    bikes: int
    docks: int
    stype: str
    zone: str | None = None
    creation_date: datetime | None = Field(default=None, alias="creationDate")
    asset_status: str = Field(alias="assetStatus")
    version: int
    update_date: datetime = Field(alias="updateDate")


class ApiDock(BaseModel):
    """Validates a dock from the getDocks response.

    `name` is the dock position number. `ledStatus`: green=empty, red=occupied.
    """

    model_config = ConfigDict(extra="ignore")

    code: str
    serial_number: str = Field(alias="serialNumber")
    name: str
    led_status: str = Field(alias="ledStatus")


class ApiBike(BaseModel):
    """Validates a bike from the getBikes response.

    `battery` is a string in API, parsed to int in transform. `parent` is dock code.
    """

    model_config = ConfigDict(extra="ignore")

    code: str
    serial_number: str = Field(alias="serialNumber")
    name: str
    battery: str | None = None
    bike_type: str | None = Field(default=None, alias="type")
    parent: str | None = None
