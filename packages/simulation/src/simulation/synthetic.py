"""Generate synthetic GIRA data from the generative model.

This is the user-facing entry point that composes models and engines
to produce synthetic station availability data matching the real GIRA
data format.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import numpy as np
    from numpy.random import Generator


def generate_single_station(
    rng: Generator,
    capacity: int,
    n_minutes: int = 1440,
) -> dict[str, np.ndarray]:
    """Generate synthetic data for a single station over one day."""
    raise NotImplementedError


def generate_multi_station(
    rng: Generator,
    n_stations: int,
    n_minutes: int = 1440,
) -> dict[str, np.ndarray]:
    """Generate synthetic data for multiple spatially-coupled stations."""
    raise NotImplementedError


def export_to_duckdb(
    data: dict[str, np.ndarray],
    output_path: Path,
) -> None:
    """Export synthetic data to a DuckDB file matching the schema contract."""
    raise NotImplementedError
