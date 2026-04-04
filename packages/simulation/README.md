# Simulation Package

Bayesian generative simulation of GIRA bicycle station dynamics. Produces synthetic station availability data from a hierarchical generative model for prior predictive checking and scenario analysis.

## Relationship to Analysis 05

This package is the production-grade version of the prototype in `.workbench/analysis/05-bayesian-generative-simulation/code/`. The prototype demonstrated a 37-parameter hierarchical model with 6 component sub-models. This package provides the installable, tested, and type-checked structure for that code.

All functions are currently stubs raising `NotImplementedError`. Lifting the prototype code is a separate future task.

## Module Structure

| Module | Description |
|--------|-------------|
| `models/demand.py` | NHPP departure/arrival rates with Fourier K=3 time-of-day profile |
| `models/dock_failure.py` | Two-level HMM: per-dock + station infrastructure failure |
| `models/bike_failure.py` | Mechanical failure fraction + battery sigmoid acceptance |
| `models/rebalancing.py` | Compound Poisson rebalancing overlay |
| `priors.py` | Prior sampling functions matching T7 specification |
| `diagnostics.py` | Prior predictive checks (D1-D4) and diagnostic plots |
| `spatial.py` | OD matrix, Haversine distances, demand substitution |
| `synthetic.py` | User-facing entry point for synthetic data generation |

## Setup

```bash
cd packages/simulation
uv sync
```

## Usage

```bash
# Run synthetic data generation (not yet implemented)
uv run python -m simulation
```

## Development

```bash
just lint       # Lint with ruff
just format     # Format with ruff
just typecheck  # Type check with pyright
just test       # Run all tests
just test-unit  # Run unit tests only
just check      # Run all quality checks (lint + typecheck + test)
```

## Environment Variables

See `.env.example`. The `MOTHERDUCK_TOKEN` is only needed when reading real observation data from MotherDuck for model fitting -- not for synthetic generation.

## Dependencies

Runtime: numpy, scipy, matplotlib, duckdb (lightweight core).

Optional `inference` extra: pymc, numpyro, arviz, jax, jaxlib. Install with `uv sync --extra inference` when implementing posterior inference.

## Status

This package is a **skeleton** -- all functions raise `NotImplementedError`. The module structure, type signatures, and test scaffolding are complete and ready for lifting the prototype code from `.workbench/analysis/05-bayesian-generative-simulation/code/`. Not wired into CI (intentionally excluded).
