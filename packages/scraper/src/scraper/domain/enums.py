"""Domain enums matching DuckDB CREATE TYPE definitions in 001_initial_schema.sql."""

import enum


class StationStatus(enum.StrEnum):
    """Station operational status. Matches SQL: station_status."""

    ACTIVE = "active"
    REPAIR = "repair"


class StationType(enum.StrEnum):
    """Station hardware type. Matches SQL: station_type."""

    A = "A"
    B = "B"


class DockState(enum.StrEnum):
    """Dock occupancy state. Matches SQL: dock_state."""

    EMPTY = "empty"
    OCCUPIED = "occupied"


class BikeType(enum.StrEnum):
    """Bike propulsion type. Matches SQL: bike_type."""

    ELECTRIC = "electric"
    CONVENTIONAL = "conventional"


class RunType(enum.StrEnum):
    """Scrape run type. Matches SQL: run_type."""

    STATION = "station"
    DETAIL = "detail"


class ExitStatus(enum.StrEnum):
    """Scrape run outcome. Matches SQL: exit_status."""

    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"
