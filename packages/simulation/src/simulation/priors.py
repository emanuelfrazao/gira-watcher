"""Prior sampling functions for the GIRA generative model.

All distributions match the prior specification table (T7) and individual
model reports (T8-T12). Each function draws a single sample or array of
samples from the specified prior.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.random import Generator


def sample_initial_occupancy_fraction(rng: Generator, size: int = 1) -> np.ndarray:
    """Beta(2.5, 7.5) -- mean 0.25, matching GIRA snapshot 23.6%."""
    raise NotImplementedError


def sample_base_departure_rate(
    rng: Generator, station_type: str = "A", size: int = 1
) -> np.ndarray:
    """Gamma prior on base departure rate (trips/hr, off-peak)."""
    raise NotImplementedError


def sample_fourier_coefficients(rng: Generator, size: int = 1) -> dict[str, np.ndarray]:
    """Sample Fourier K=3 coefficients for the departure daily profile."""
    raise NotImplementedError


def sample_dock_transition_params(rng: Generator, size: int = 1) -> dict[str, np.ndarray]:
    """Sample dock HMM transition parameters from T7/T9 priors."""
    raise NotImplementedError
