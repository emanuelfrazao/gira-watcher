"""Spatial model for multi-station GIRA simulation.

Implements:
  - Haversine pairwise distance computation
  - Gravity-model OD matrix (T13 Section 3)
  - Spatially correlated demand rates (simplified BYM2 via multivariate normal)
  - Demand substitution (frustrated users walk to nearest non-empty station)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.random import Generator


def haversine_distance_matrix(lats: np.ndarray, lons: np.ndarray) -> np.ndarray:
    """Compute pairwise Haversine distances in meters."""
    raise NotImplementedError


def build_od_matrix(
    dist_matrix: np.ndarray,
    capacities: np.ndarray,
    beta_dist: float,
    alpha_elev: float = 0.0,
    elevation_diffs: np.ndarray | None = None,
) -> np.ndarray:
    """Build origin-destination probability matrix using gravity model."""
    raise NotImplementedError


def sample_spatially_correlated_rates(
    rng: Generator,
    dist_matrix: np.ndarray,
    mu_log_rate: float,
    sigma_spatial: float,
    corr_range_m: float,
) -> np.ndarray:
    """Sample spatially correlated base departure rates for all stations."""
    raise NotImplementedError


def compute_substitution_probs(
    station_idx: int,
    dist_matrix: np.ndarray,
    delta_subst: float = 500.0,
) -> np.ndarray:
    """Compute substitution probabilities for a frustrated user at station_idx."""
    raise NotImplementedError
