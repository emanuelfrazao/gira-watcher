"""Compound Poisson rebalancing overlay for station simulation.

From T10 Section 5:
  Events arrive at rate phi_station(t) = phi_base * g_rebal(h)
  Each event moves Poisson(mu_batch) + 3 bikes
  Direction: add bikes if below target, remove if above target
  Target occupancy: ~40% of capacity
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.random import Generator


def rebalancing_tod_profile(hours: np.ndarray) -> np.ndarray:
    """Rebalancing time-of-day profile g_rebal(h).

    60% during 1:00-5:00, 40% during 10:00-15:00. Normalized so integral
    over 24h = 1.
    """
    raise NotImplementedError


def generate_rebalancing_event(
    rng: Generator,
    minute: int,
    rate_per_day: float,
    mu_batch: float,
    current_occupancy: int,
    capacity: int,
    target_fraction: float = 0.4,
) -> int:
    """Check for and generate a rebalancing event at this minute."""
    raise NotImplementedError
