"""Dock failure HMM model for station simulation.

Implements the two-level failure hierarchy from T9:
  Level 1: Per-dock binary HMM (operational / failed)
  Level 2: Station infrastructure binary HMM (normal / failed)

Effective dock state: s_eff = s_dock * s_infra
Effective capacity: K_eff = sum of s_eff across docks
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.random import Generator


def init_dock_states(
    rng: Generator,
    n_docks: int,
    p_break: float,
    p_repair: float,
) -> np.ndarray:
    """Initialize dock states from stationary distribution."""
    raise NotImplementedError


def step_dock_hmm(
    rng: Generator,
    dock_states: np.ndarray,
    p_break: float,
    p_repair: float,
) -> np.ndarray:
    """Advance dock states by one 5-minute HMM step."""
    raise NotImplementedError


def step_infra_hmm(
    rng: Generator,
    infra_state: int,
    p_infra_fail: float,
    p_infra_restore: float,
) -> int:
    """Advance station infrastructure state by one 5-minute step."""
    raise NotImplementedError


def compute_effective_capacity(
    dock_states: np.ndarray,
    infra_state: int,
) -> int:
    """Compute K_eff = s_infra * sum(s_dock)."""
    raise NotImplementedError
