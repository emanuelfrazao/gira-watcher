# GIRA Watch

### Transparent Public Accountability for Lisbon’s Shared Bicycle System

-----

|              |                                     |
|--------------|-------------------------------------|
|**Status**    |Draft — v0.2                         |
|**Date**      |April 2026                           |
|**Nature**    |Investigative Journalism / Civic Tech|
|**Scope**     |Lisbon, Portugal                     |
|**Repository**|Public (GitHub)                      |

-----

## 0. Executive Summary

GIRA Watch is an open, fully transparent data collection and analysis project targeting the GIRA shared bicycle system operated in Lisbon. The project’s goal is to produce rigorous, evidence-based statistics on the operational reliability of GIRA — specifically the availability of bikes and the functional state of docking stations across the city — and to make those findings public.

The project is grounded in three principles: **radical transparency** (every line of code, every deployment step, and every raw data point is public), **methodological integrity** (metrics are defined before analysis begins, preventing cherry-picking), and **reproducibility** (any person or institution can clone the repository and reproduce the full pipeline independently).

> GIRA Watch does not exploit any private or authenticated endpoint. It queries the same public API used by GIRA’s own mobile application and by third-party wrappers such as GIRA+. No user data is collected. No authentication is bypassed.

-----

## 1. Context & Motivation

### 1.1 What is GIRA?

GIRA is Lisbon’s municipal shared bicycle network, operated by a private company under public concession. It provides docking stations distributed across the city from which residents and visitors can rent electric and mechanical bicycles. As a public-service concession, GIRA’s operational performance is a matter of legitimate public interest.

### 1.2 The Problem

Widespread anecdotal reports from residents suggest that a significant proportion of GIRA docking stations are persistently empty or have bikes that are locked or malfunctioning and cannot be released. The company’s own application is reported to have UX and reliability problems. Third-party apps (e.g. GIRA+) were built precisely because users found the official app insufficient.

No publicly available, systematic, time-series data exists to either confirm or refute these claims. GIRA Watch exists to produce that data.

### 1.3 Why This Matters

- GIRA operates under a public concession — taxpayers and city governance have a right to know if service-level obligations are being met.
- Journalism and civil society cannot hold concession operators accountable without evidence.
- The methodology and full dataset will be open so that academics, journalists, and city officials can all use and scrutinise the findings.

-----

## 2. Transparency Principles

Transparency is not a feature of this project — it is the project.

|Principle                 |What it means in practice                                                                                                                               |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Code is the deployment**|The GitHub Actions workflow YAML that lives in the public repository IS the deployment definition. There is no hidden server configuration.             |
|**Immutable run logs**    |Every execution is logged publicly in the GitHub Actions tab, linking each run to the exact commit SHA that produced it.                                |
|**Pre-registered metrics**|All statistical metrics are defined and committed to the repository before any analysis is run. This prevents post-hoc selection of convenient metrics. |
|**Open raw data**         |Every raw scrape result is stored in a public, queryable database. Anyone can attach and query the full dataset directly from their own DuckDB instance.|
|**Reproducibility**       |Any third party can fork the repository, point it at the same public API and public database, and reproduce every finding independently.                |

-----

## 3. Pre-Registered Methodology

> These metrics are locked before collection begins. Changing them after data has been collected would compromise the integrity of the project and would be documented as a methodological revision in the repository’s commit history.

### 3.1 Data Source

The GIRA mobile application communicates with an internal REST API to display real-time station status. This API is unauthenticated and publicly reachable — the same endpoints used by third-party applications such as GIRA+. GIRA Watch queries these endpoints. No credentials, tokens, or private access of any kind are used.

### 3.2 Collection Parameters

- **Frequency:** every 5 minutes (GitHub Actions minimum schedule interval)
- **Coverage:** all docking stations returned by the stations list endpoint (~200 stations)
- **Fields collected per station per snapshot:** station ID, station name, coordinates, total docks, available bikes (mechanical), available bikes (electric), available empty docks, timestamp of query
- **No user data, trip data, or personally identifiable information** is collected or stored
- **Minimum collection period before publication of findings:** 90 days

### 3.3 Pre-Registered Metrics

#### Dock Empty Rate

For each station: the percentage of observations where `available_bikes = 0`. Reported as a daily average and a rolling 30-day average. A station is classified as *chronically unavailable* if its 30-day empty rate exceeds 70%.

#### System-Wide Availability

At each 5-minute interval: `(sum of available bikes across all stations) / (sum of total docks across all stations)`. Reported as hourly and daily averages. Decomposed by bike type (mechanical vs electric).

#### Peak-Hour Desert Index

Morning peak defined as 07:30–09:30 local time, Monday–Friday. Evening peak defined as 17:30–19:30 local time, Monday–Friday. For each station: empty rate during peak hours specifically, compared to its overall empty rate. Stations with empty rate > 80% during peaks are flagged.

#### Dead Dock Detector

A station is flagged as potentially reporting phantom availability if its non-zero bike count remains exactly constant for more than 4 consecutive hours. This pattern is inconsistent with normal usage and suggests bikes are physically locked or the API is returning stale data. Flagged observations are reported separately and excluded from availability statistics.

#### Dock Functional Rate

For each station: `(total docks) - (available bikes) - (available empty docks) = docks in unknown/broken state`. Reported as a percentage of total capacity. A station where `broken_docks / total_docks > 50%` for more than 14 consecutive days is classified as *structurally degraded*.

-----

## 4. Technical Architecture

### 4.1 Repository Structure

|Path                          |Purpose                                                               |
|------------------------------|----------------------------------------------------------------------|
|`.github/workflows/scrape.yml`|Cron schedule and scraper execution — the public deployment definition|
|`scraper/main.py`             |Fetches GIRA API, validates response, writes to MotherDuck            |
|`scraper/schema.py`           |Data model and field definitions                                      |
|`dashboard/app.py`            |Streamlit statistics dashboard (Python only)                          |
|`dashboard/queries.py`        |All SQL queries used in the dashboard, fully readable                 |
|`analysis/notebooks/`         |Jupyter notebooks for producing findings                              |
|`METHODOLOGY.md`              |This methodology, version-controlled                                  |
|`README.md`                   |Project overview, links to live dashboard and dataset                 |

### 4.2 Scraping Layer — GitHub Actions

The scraper runs as a GitHub Actions scheduled workflow. The schedule is defined in `.github/workflows/scrape.yml` in the public repository. Every execution is publicly logged in the Actions tab, including: the exact commit SHA of the code that ran, start and end timestamps, exit status, and full stdout/stderr output.

Each scrape writes a run manifest alongside the data: `{ run_id, commit_sha, github_run_url, timestamp_utc, stations_queried, records_written }`. This creates a publicly auditable chain of custody from source code to stored data.

> **Why GitHub Actions?** The workflow YAML in the repository IS the deployment. There is no hidden server, no separate CI configuration, and no divergence possible between what is published and what runs. Anyone can fork the repository and obtain identical behaviour.

### 4.3 Storage — MotherDuck (DuckDB in the cloud)

Raw scrape results are stored in MotherDuck, the cloud-hosted version of DuckDB, with a public share URL. MotherDuck is a columnar, analytical database (OLAP) — the correct engine for append-only time-series data with heavy aggregation queries.

**Why MotherDuck over a traditional database (e.g. PostgreSQL/Supabase):**

|                      |PostgreSQL            |MotherDuck (DuckDB)      |
|----------------------|----------------------|-------------------------|
|Engine type           |OLTP — row-oriented   |OLAP — columnar          |
|Storage efficiency    |Low for time-series   |Extreme compression      |
|Analytical query speed|Moderate              |Fast by design           |
|Free tier             |~500 MB               |10 GB post-compression   |
|Public data sharing   |REST API only         |Native `ATTACH` share URL|
|Dev/prod parity       |Separate client needed|Same DuckDB client       |

DuckDB’s columnar compression means the full 90-day dataset will likely fit comfortably within the free tier. Development happens locally with plain DuckDB; production points to MotherDuck by changing one line — the connection string.

**Public access:** MotherDuck’s `CREATE SHARE` generates a URL that anyone can use to `ATTACH` the database directly in their own DuckDB instance and run arbitrary SQL against the raw data. This goes beyond a REST API — it is full, first-class database access with no intermediary.

The primary table schema:

```sql
CREATE TABLE observations (
    id            BIGINT PRIMARY KEY,
    station_id    VARCHAR,
    station_name  VARCHAR,
    lat           DOUBLE,
    lon           DOUBLE,
    total_docks   INTEGER,
    bikes_mech    INTEGER,
    bikes_elec    INTEGER,
    empty_docks   INTEGER,
    queried_at    TIMESTAMPTZ,
    run_id        VARCHAR,
    commit_sha    VARCHAR
);
```

### 4.4 Dashboard — Streamlit on Streamlit Community Cloud

A statistics dashboard is built in Python using Streamlit. It connects directly to the public MotherDuck share. The dashboard is deployed via Streamlit Community Cloud, which deploys directly from the GitHub repository — the deployed application is always the code at a specified branch and file path, both publicly visible.

The dashboard displays the five pre-registered metrics defined in Section 3, updated on each page load. All SQL queries powering the charts are readable in `dashboard/queries.py`.

> **Why Streamlit?** It requires no frontend code, runs entirely in Python (the same language as the scraper), lives in the same repository, and its Community Cloud deployment is as transparent as GitHub Actions — the source is always a specific commit in a public repo.

### 4.5 Verification Chain

|What to verify        |How to verify it                                                           |
|----------------------|---------------------------------------------------------------------------|
|Collection logic      |Read `scraper/main.py` in the public repository                            |
|What actually ran     |Read `.github/workflows/scrape.yml` — this is the deployment               |
|That each run executed|GitHub Actions tab → public log per execution                              |
|That run = that code  |Commit SHA in each run log links to exact source version                   |
|Raw data integrity    |Attach MotherDuck share in your own DuckDB; compare `run_id` to Actions log|
|Dashboard queries     |Read `dashboard/queries.py` — no hidden transformations                    |
|Metric definitions    |Read `METHODOLOGY.md` — committed before data collection                   |

-----

## 5. Legal & Ethical Considerations

### 5.1 API Access

The GIRA API queried by this project is the same API used by GIRA’s own official mobile application. It requires no authentication, no API key, and no account. It is, by technical definition, a public endpoint. Third-party applications (GIRA+, etc.) have queried the same API without objection.

Querying a public, unauthenticated API is not hacking, not a breach of computer security law, and is standard practice in data journalism. The project makes no attempt to access any authenticated endpoint, internal system, database, or administrative interface.

### 5.2 Rate Limiting & Responsible Scraping

The scraper runs at one request per station per 5-minute interval, with sequential requests and a brief delay between each. This is a very low request rate compared to normal user traffic. The scraper does not attempt to circumvent any rate limiting or anti-scraping measures.

### 5.3 Data Minimisation

Only station-level operational data is collected. No user data, trip data, personal data, or session data is stored. The project is fully compliant with data minimisation principles under GDPR, as the data collected pertains entirely to infrastructure, not individuals.

### 5.4 Public Interest Justification

GIRA operates under a public concession in Lisbon. The assessment of its operational performance is a matter of direct public interest. The journalistic purpose of this project — providing citizens, journalists, and municipal authorities with objective evidence of service quality — constitutes legitimate public interest activity.

-----

## 6. Architectural Decision Record

### ADR-001 — GitHub Actions as scheduler (not a private server)

- **Decision:** Use GitHub Actions scheduled workflows instead of a private VPS or cloud function.
- **Rationale:** A private server creates an unverifiable black box — the public cannot confirm that what runs matches the published code. GitHub Actions makes the deployment definition part of the public repository, and makes every execution publicly logged and commit-linked.
- **Trade-off:** GitHub Actions minimum schedule interval is 5 minutes, not 1. Acceptable for the analytical goals of the project.

### ADR-002 — MotherDuck for storage (not PostgreSQL/Supabase)

- **Decision:** Store data in MotherDuck (cloud DuckDB) with a public share, not in a PostgreSQL instance.
- **Rationale:** PostgreSQL is a row-oriented OLTP engine — wrong for append-only time-series analytics. DuckDB’s columnar compression dramatically reduces storage footprint (benchmarks show 10–12× compression on similar data). The native `ATTACH` share provides richer public access than a REST API. Dev/prod parity is achieved by changing only the connection string.
- **Trade-off:** MotherDuck is less mature than PostgreSQL. Mitigated by periodically exporting Parquet snapshots to the repository’s releases for archival and as a fallback.

### ADR-003 — Streamlit for the dashboard (not a JS frontend)

- **Decision:** Build the public statistics dashboard in Streamlit (Python), not a JavaScript framework.
- **Rationale:** The project is Python-only. Adding a JS frontend would create a second language, a separate deployment pipeline, and additional complexity that reduces transparency. Streamlit Community Cloud deploys directly from the GitHub repo, maintaining the same code-is-deployment guarantee as GitHub Actions.
- **Trade-off:** Streamlit dashboards are less customisable than bespoke frontends. Acceptable given the goal is data transparency, not visual polish.

### ADR-004 — Pre-registration of metrics

- **Decision:** All statistical metrics are formally defined and committed to `METHODOLOGY.md` before any data collection begins.
- **Rationale:** Post-hoc metric selection is the most common way data journalism projects introduce bias, even unintentionally. Committing metrics before data exists makes the project structurally resistant to this failure mode, and provides a credible answer to critics who might otherwise allege cherry-picking.
- **Trade-off:** Any revision to metrics after collection starts must be documented as a formal amendment with rationale. This is a feature, not a bug.

-----

## 7. Indicative Timeline

|Phase        |Activities                                                                                                                      |
|-------------|--------------------------------------------------------------------------------------------------------------------------------|
|**Week 1–2** |Set up repository, write scraper, configure MotherDuck schema, deploy GitHub Actions, commit `METHODOLOGY.md` — begin collection|
|**Week 2–4** |Monitor scraper reliability, fix edge cases, build initial Streamlit dashboard with live metrics                                |
|**Month 2–3**|Continue collection, make raw data and dashboard publicly accessible, share with interested journalists and civic groups        |
|**Month 3+** |Run analysis notebooks on 90-day dataset, produce findings report, publish                                                      |

-----

*GIRA Watch is an open project. Contributions, scrutiny, and independent reproduction are welcome.*
