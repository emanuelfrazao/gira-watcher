# Contributing to GIRA Watch

Thank you for your interest in contributing. This document covers the development setup, conventions, and workflow for the project.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| [uv](https://docs.astral.sh/uv/) | Python package management (scraper, simulation) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Node.js](https://nodejs.org/) + npm | Website development | [nodejs.org](https://nodejs.org/) (LTS recommended) |
| [just](https://github.com/casey/just) | Task runner (all packages) | `brew install just` / `cargo install just` |
| [DuckDB CLI](https://duckdb.org/docs/installation/) | Database schema development (optional) | `brew install duckdb` |

## Repository Structure

```
packages/
  db/           SQL-only schema package (DuckDB migrations)
  scraper/      Python data collection pipeline
  simulation/   Python Bayesian simulation (optional)
  website/      SvelteKit 2 dashboard on Vercel
```

Each package is independent -- no cross-package imports. The SQL migrations in `packages/db/` are the integration contract.

## Per-Package Development

### Database (`packages/db/`)

```bash
cd packages/db
just apply          # Apply all migrations to local DuckDB
just seed           # Apply migrations + load test fixtures
just reset          # Drop and recreate from scratch
just check          # Validate SQL against in-memory DuckDB
just lint           # Lint SQL with SQLFluff
just validate       # Both lint + check
```

### Scraper (`packages/scraper/`)

```bash
cd packages/scraper
uv sync --all-extras   # Install dependencies
just check             # Run all quality checks (lint + typecheck + test)
just lint              # Lint with ruff
just format            # Auto-fix lint + format
just typecheck         # Type-check with pyright (strict mode)
just test              # Run all tests
just test-unit         # Run unit tests only
just test-integration  # Run integration tests only
just run --run-type station  # Run scraper locally
```

### Website (`packages/website/`)

```bash
cd packages/website
npm install            # Install dependencies
just check             # Type-check (svelte-check + TypeScript)
just test              # Run tests (vitest)
just dev               # Start development server
just build             # Production build
just preview           # Preview production build
just format            # Format with Prettier
```

### Simulation (`packages/simulation/`)

```bash
cd packages/simulation
uv sync                # Install dependencies
just check             # Run all quality checks (lint + typecheck + test)
just lint              # Lint with ruff
just format            # Format with ruff
just typecheck         # Type-check with pyright
just test              # Run all tests
```

## Development Conventions

### Python (scraper, simulation)

- **Type hints** on all function signatures and class attributes
- **Strict pyright** (`typeCheckingMode = "strict"`)
- **Ruff** for linting and formatting (`line-length = 100`, target Python 3.11)
- Lint rules: `F, E, W, I, UP, C4, SIM, PTH, RET, TCH`
- Built-in generics (`list[str]`, `dict[str, int]`), `Optional[str]` for nullable
- `pathlib.Path` over `os.path`, f-strings for formatting
- Absolute imports only, grouped: stdlib / third-party / local
- `Pydantic BaseModel` for API response validation, `dataclass` for internal data, `TypedDict` for DuckDB row shapes

### TypeScript (website)

- **Strict mode** in `tsconfig.json`
- **svelte-check** for Svelte component type-checking

### Error Handling

- Custom exception hierarchy (Python): `GiraWatchError` base class
- Never bare `except:` -- always specify the exception type
- Never silently swallow errors -- log with context, then re-raise or propagate
- Keep `try` blocks small and focused

### Testing

- **Unit tests** (`@pytest.mark.unit`): pure logic, no external dependencies
- **Integration tests** (`@pytest.mark.integration`): real in-memory DuckDB, mocked HTTP responses
- Test behaviour, not implementation
- `@pytest.mark.parametrize` for multiple input scenarios
- Website tests use vitest

## PR Workflow

### Branch Naming

```
feat/<short-description>
fix/<short-description>
docs/<short-description>
refactor/<short-description>
```

### Commit Messages

All commits follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

feat(scraper): add JWT authentication flow
fix(website): correct empty rate calculation
docs: update METHODOLOGY.md with amendment
ci(scraper): add integration test step
test(db): add seed data for dock snapshots
refactor(scraper): extract storage protocol
chore: update dependencies
```

**Types:** `feat`, `fix`, `docs`, `ci`, `test`, `refactor`, `chore`, `perf`

**Scopes** (optional but encouraged): `scraper`, `website`, `db`, `simulation`, `infra`

### Before Submitting

Run the quality checks for every package you changed:

```bash
# Python packages
just check   # runs lint + typecheck + test

# Website
just check   # runs svelte-check
just test    # runs vitest

# Database
just validate  # runs lint + check
```

### Versioning

The project uses SemVer v0.x (single version in root `pyproject.toml`). MINOR bumps signal breaking or significant changes; PATCH bumps signal backward-compatible fixes. Changelog is generated by git-cliff from commit history.

## Questions?

Open a GitHub issue in this repository for bugs, feature requests, or questions about the codebase.
