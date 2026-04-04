# gira-watcher

Open civic-tech project that scrapes, stores, and analyses GIRA (Lisbon) bicycle station availability using the public API — producing a transparent, reproducible accountability dataset.

## Commands

```bash
# Environment
uv sync                          # Install all dependencies
uv add <package>                 # Add a dependency

# Quality
uv run pyright                   # Type check
uv run ruff check --fix .        # Lint with auto-fix
uv run ruff format .             # Format
uv run pytest                    # All tests
uv run pytest -m unit            # Unit tests only
uv run pytest -m integration     # Integration tests only

# Scraper
uv run python -m scraper.main    # Run scraper locally (writes to local DuckDB)

# Dashboard
uv run streamlit run dashboard/app.py   # Run dashboard locally
```

## Project Structure

```
gira-watcher/
├── .github/
│   └── workflows/
│       └── scrape.yml       # Cron scheduler — the public deployment definition (every 5 min)
├── scraper/
│   ├── main.py              # Fetch GIRA API → validate → write to MotherDuck
│   └── schema.py            # Response schema, field definitions, Pydantic models
├── dashboard/
│   ├── app.py               # Streamlit application — renders the five pre-registered metrics
│   └── queries.py           # All SQL queries (imported by app.py; no inline SQL elsewhere)
├── analysis/
│   └── notebooks/           # Jupyter notebooks for 90-day findings report
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── spec/                    # Planning artifacts (VISION, SPEC, PLAN)
├── METHODOLOGY.md           # Pre-registered metric definitions — committed before first run
├── AGENTS.md                # This file
├── CLAUDE.md                # Symlink → AGENTS.md
└── pyproject.toml
```

## Architecture

**Pipeline**: GitHub Actions cron → `scraper/main.py` → MotherDuck (DuckDB) → Streamlit dashboard / public `ATTACH` share.

Every scrape run writes to two tables:
- `observations` — one row per station per run (append-only time-series)
- `scrape_runs` — one row per execution with `run_id`, `commit_sha`, `github_run_url`

This creates a public, auditable chain of custody: every data point can be traced to its exact source commit and GitHub Actions log.

### Entrypoints

| Entrypoint | Purpose |
|-----------|---------|
| `scraper/main.py` | CLI entry for the scraper; invoked by GitHub Actions |
| `dashboard/app.py` | Streamlit app; run locally or deployed on Streamlit Community Cloud |
| `.github/workflows/scrape.yml` | The deployment definition — what actually runs in production |

### External Services

| Service | Role | Auth |
|---------|------|------|
| GIRA public REST API | Data source — station states | None (unauthenticated) |
| MotherDuck | Columnar cloud storage; public `ATTACH` share | `MOTHERDUCK_TOKEN` secret (write); share URL (read) |
| GitHub Actions | Scheduler, public execution log | GitHub repo secrets |
| Streamlit Community Cloud | Dashboard hosting | Connected to GitHub repo |

### Connection Strings

The scraper uses one connection string, selected by environment:

```python
# Local development
conn = duckdb.connect("gira_local.duckdb")

# Production (GitHub Actions)
conn = duckdb.connect(f"md:gira?motherduck_token={token}")
```

Only the connection string changes between environments — all other scraper logic is identical.

## Development Practices

### Design

- **Deep modules**: hide implementation complexity behind simple, stable interfaces
- **Single responsibility**: one clear reason to change per module, class, and function
- **YAGNI / KISS**: no features or abstractions until there is a concrete need
- **DRY**: extract common logic, but don't over-abstract for only 2 occurrences
- Business logic must be independent of infrastructure (DuckDB, Streamlit, GitHub Actions)

### Python Tooling

Use **uv** for package management, **ruff** for lint/format, **pyright** for types, **pytest** for tests.

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["F", "E", "W", "I", "UP", "C4", "SIM", "PTH", "RET", "TCH"]

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.11"
include = ["src"]
reportMissingTypeStubs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--strict-markers", "--strict-config"]
markers = [
    "unit: Unit tests (no external deps)",
    "integration: Integration tests (real DuckDB, mocked GIRA API)",
]
```

### Type System

- Type hints on all function signatures and class attributes
- Built-in generics: `list[str]`, `dict[str, int]` (not `typing.List`)
- `Optional[str]` for nullable — not `str | None`
- `Protocol` for structural subtyping; `TypeAlias` for complex nested types
- **Pydantic `BaseModel`** for GIRA API response validation (external boundary)
- **`dataclass`** for internal data objects (e.g., `ObservationRow`)
- **`TypedDict`** for dict-shaped data passed to DuckDB

### Idiomatic Python

- `pathlib.Path` over `os.path`
- f-strings for formatting
- Comprehensions for transformations; generators for large datasets
- Context managers (`with`) for DuckDB connections and file I/O
- `enum.Enum` for fixed value sets (e.g., `ExitStatus`)
- `match`/`case` for multi-branch conditional logic (3.10+)

### Error Handling

- Custom exception hierarchy: `GiraWatchError` → `GiraApiError`, `StorageError`, etc.
- Never bare `except:` — always specify exception type
- Never silently swallow errors — log with context, then re-raise or propagate
- Keep `try` blocks small and focused
- Log the `run_id` in every error message from the scraper for traceability

### Testing

- `tests/unit/` — pure logic, no external dependencies; mock the DuckDB connection and GIRA HTTP client
- `tests/integration/` — real in-memory DuckDB, mocked GIRA HTTP responses (no network calls)
- `@pytest.mark.parametrize` for multiple input scenarios
- Fixtures in `conftest.py` for shared database setup
- Test behaviour, not implementation

### Imports

- Absolute imports only
- Group: stdlib → third-party → local (blank lines between groups)

### Pre-Commit Checklist

```bash
uv run pyright
uv run ruff check --fix . && uv run ruff format .
uv run pytest
```

### Versioning

- **SemVer v0.x**: MINOR bumps signal breaking or significant changes; PATCH bumps signal backward-compatible fixes. This is explicitly declared — the SemVer spec leaves v0.x semantics open.
- **Conventional Commits**: All commit messages follow [Conventional Commits 1.0](https://www.conventionalcommits.org/). Prefixes: `feat:`, `fix:`, `docs:`, `ci:`, `test:`, `refactor:`, `chore:`, `perf:`. Scopes optional but encouraged: `feat(scraper):`, `fix(website):`.
- **Single repo version**: One version covers the whole system in `pyproject.toml [project] version`. No per-package versioning.
- **Changelog**: Generated by `git-cliff` from Conventional Commit history. Config in `pyproject.toml [tool.git-cliff.*]`.
- **Release protocol**: Tag-first workflow — `bump-my-version bump <patch|minor>` updates `pyproject.toml` + creates git tag → push tag → GitHub Actions `release.yml` runs git-cliff and publishes a GitHub Release via `softprops/action-gh-release`.
- **Starting point**: `v0.1.0` after the project skeleton is complete.

## Project-Specific Instructions

### Transparency is a hard constraint

- `METHODOLOGY.md` must be committed before any scrape run writes data. Never modify it without a documented rationale commit.
- `dashboard/queries.py` is the single source of truth for all SQL. **No inline SQL in `dashboard/app.py`** — ever. This ensures every query powering the dashboard is publicly readable in one place.
- Every scrape run must write a row to `scrape_runs` with `run_id`, `commit_sha`, and `github_run_url`. A run with no manifest record breaks the audit chain.

### Pre-registered metrics — do not add new ones silently

The five metrics (Dock Empty Rate, System-Wide Availability, Peak-Hour Desert Index, Dead Dock Detector, Dock Functional Rate) are pre-registered. Adding or changing a metric after data collection has begun is a methodological amendment — it requires a separate commit with a rationale, and a note in `METHODOLOGY.md`.

### GIRA API is undocumented and unauthenticated

- Validate the response shape in `scraper/schema.py` using Pydantic before writing anything to the database
- If validation fails, write `exit_status = 'error'` to `scrape_runs` and exit non-zero — do not write partial `observations` from a malformed response
- Log the raw response (truncated) on validation failure so the Actions log captures evidence of API drift

### DuckDB connection pattern

- Local dev: plain file (`gira_local.duckdb`)
- Production: MotherDuck URL from `MOTHERDUCK_TOKEN` env var
- The scraper reads the token from the environment; it is never hardcoded or logged
- The dashboard connects to the **public read-only share** — it never uses the write token

### Dead Dock Detector exclusion

Observations flagged by the Dead Dock Detector (constant non-zero bike count for >4 consecutive hours) are **excluded from all availability metrics**. SQL queries in `dashboard/queries.py` must always filter these out. Document the exclusion logic in the query comment.

### Spec artifacts

Planning documents live in `spec/`. Key files:
- [`spec/VISION.md`](spec/VISION.md) — problem, users, success criteria
- [`spec/SPEC.md`](spec/SPEC.md) — domain model, data contracts, architecture
- [`spec/PLAN.md`](spec/PLAN.md) — milestones, task table, risk register
