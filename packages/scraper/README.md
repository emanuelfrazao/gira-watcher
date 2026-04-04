# GIRA Scraper

Data collection pipeline for GIRA (Lisbon) bicycle station availability. Polls the GIRA API, validates responses with Pydantic, transforms data into the normalized schema, and writes to DuckDB storage.

## Setup

```bash
uv sync --all-extras
```

## Development

```bash
just check        # Run all quality checks (lint + typecheck + test)
just lint         # Lint with ruff
just format       # Auto-fix lint and format
just typecheck    # Type-check with pyright (strict)
just test         # Run all tests
just test-unit    # Run unit tests only
just test-integration  # Run integration tests only
just run --run-type station  # Run scraper locally
```

## Module Architecture

```
src/scraper/
  domain/         # Enums, dataclasses, TypedDicts, errors
    enums.py      # StrEnums matching DuckDB CREATE TYPE definitions
    models.py     # Frozen dataclasses: dimensions, snapshots, RunManifest, WriteResult
    typed_dicts.py  # TypedDicts for DuckDB INSERT row shapes
    errors.py     # Two-level exception hierarchy (GiraWatchError base)
  api/            # GIRA API client and Pydantic validation models
    schema.py     # ApiStation, ApiDock, ApiBike (Pydantic BaseModel)
    client.py     # GiraClient: async HTTP client with lazy JWT auth
  storage/        # Swappable storage backends via Protocol pattern
    protocol.py   # StorageBackend + RunWriter Protocols
    motherduck.py # MotherDuck (cloud DuckDB) backend
    local.py      # Local DuckDB file backend
    parquet.py    # Parquet-to-R2 fallback backend
  orchestrator.py # Wires client -> transform -> storage
  transform.py    # API -> domain model mapping (6 functions)
  audit.py        # repository_dispatch notification to audit repo
  main.py         # CLI entrypoint: --run-type {station,detail}
```

## Environment Variables

See `.env.example` for the full list. Key variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GIRA_STORAGE_URL` | Yes | DuckDB connection string |
| `GIRA_STORAGE_TOKEN` | For MotherDuck | MotherDuck auth token |
| `GIRA_API_EMAIL` | For detail runs | GIRA account email |
| `GIRA_API_PASSWORD` | For detail runs | GIRA account password |
| `GIRA_SCHEDULER_IDENTITY` | No | Identifies the scheduler (default: `local-dev`) |
| `GIRA_COMMIT_SHA` | No | Git commit SHA for traceability |
| `GITHUB_AUDIT_TOKEN` | No | GitHub PAT for audit dispatch |
| `GITHUB_AUDIT_REPO` | No | Target repo for audit events |

## Status

This package is a **skeleton** -- all business logic raises `NotImplementedError`. The structure, interfaces, types, and test scaffolding are complete and ready for implementation.
