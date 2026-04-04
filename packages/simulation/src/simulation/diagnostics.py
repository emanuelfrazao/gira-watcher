"""Prior predictive check diagnostics for the GIRA simulation.

Implements diagnostic criteria from T6 Section 3:
  D1: Bounds check (occupancy in [0, K_eff])
  D2: Rate plausibility (trips/hr in [0.1, 20])
  D3: Daily cycle (CV of hourly occupancy > 0.05)
  D4: Stationarity / non-degeneracy (occupancy not stuck at boundary)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import numpy as np


def check_d1_bounds(occupancy: np.ndarray, k_eff: np.ndarray) -> dict[str, object]:
    """D1: Occupancy stays in [0, K_eff] for all draws."""
    raise NotImplementedError


def check_d2_rate_plausibility(
    departures: np.ndarray, n_minutes: int
) -> dict[str, object]:
    """D2: Implied trips/station/hr should be in [0.1, 20]."""
    raise NotImplementedError


def check_d3_daily_cycle(occupancy: np.ndarray) -> dict[str, object]:
    """D3: CV of hourly mean occupancy > 0.05."""
    raise NotImplementedError


def plot_occupancy_traces(
    occupancy_draws: np.ndarray,
    title: str,
    output_path: Path,
    n_traces: int = 20,
) -> None:
    """Plot occupancy time series for a sample of draws."""
    raise NotImplementedError
