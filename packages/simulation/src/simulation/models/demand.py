"""NHPP demand generation for station simulation.

Implements time-varying departure and arrival rates from T10:
  lambda_dep(t) = lambda_base * f_tod(h) * f_dow(d) * (1 + xi)
  lambda_arr(t) = lambda_dep(t) * (1 + epsilon)

Time-of-day modulation uses Fourier K=3 harmonics (T10 Section 3.3).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.random import Generator


def fourier_tod_profile(hours: np.ndarray, coeffs: dict[str, float]) -> np.ndarray:
    """Compute time-of-day modulation f_tod(h) using Fourier K=3 harmonics."""
    raise NotImplementedError


def compute_departure_rates(
    minutes: np.ndarray,
    lambda_base: float,
    fourier_coeffs: dict[str, float],
    is_weekend: bool = False,
    r_weekend: float = 0.42,
    xi: float = 0.0,
) -> np.ndarray:
    """Compute departure rate lambda_dep(t) at each minute."""
    raise NotImplementedError


def compute_arrival_rates(
    departure_rates: np.ndarray,
    epsilon: float = 0.0,
) -> np.ndarray:
    """Compute arrival rates from departure rates."""
    raise NotImplementedError


def generate_demand_events(
    rng: Generator,
    dep_rates: np.ndarray,
    arr_rates: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate Poisson demand event counts at each minute."""
    raise NotImplementedError
