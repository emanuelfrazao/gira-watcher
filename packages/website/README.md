# GIRA Watch Website

SvelteKit 2 data dashboard for GIRA Watch. Displays pre-registered availability metrics, station explorer, interactive maps, and editorial data stories. Deployed on Vercel with ISR caching.

## Setup

```bash
npm install
```

## Development

```bash
just dev        # Start development server
just build      # Production build
just preview    # Preview production build locally
just check      # Type-check (svelte-check + TypeScript)
just test       # Run tests (vitest)
just lint       # Lint (svelte-check)
just format     # Format with Prettier
```

## Module Architecture

```
src/
  lib/
    server/
      db.ts               Pool singleton (pg -> MotherDuck via Postgres wire protocol)
      queries/
        kpi.ts             System-wide KPI aggregates
        availability.ts    System-Wide Availability time series
        empty-rate.ts      Dock Empty Rate per station
        desert-index.ts    Peak-Hour Desert Index
        dead-dock.ts       Dead Dock Detector flags
        functional-rate.ts Dock Functional Rate
        analytics.ts       Cross-metric analytics
        fleet.ts           Fleet health (bike battery, type breakdown)
        audit.ts           Scrape run audit trail
        geo.ts             Station coordinates for map rendering
        station.ts         Station detail queries
    types/
      enums.ts             Enum types matching DuckDB CREATE TYPE
      dimensions.ts        Station, Dock, Bike interfaces
      facts.ts             Snapshot interfaces
      metrics.ts           Metric result shapes
      chart-data.ts        Observable Plot data structures
      filters.ts           Filter state types
      api.ts               API route response types
      audit.ts             Audit trail types
    components/
      layout/              Header, Footer, FilterBar, FilterChips, Breadcrumb
      charts/              TimeSeries, Heatmap, StackedBar, RankedTable, GanttTimeline, Sparkline, BoxPlot, DivergingBar, PlotContainer
      map/                 StationMap, MapPopup, MapLegend, TimeLapse
      station/             KpiCard, KpiStrip, StationCard, StationHeader, ComparisonSelector
      editorial/           ScrollySection, Annotation, CalloutBox, MethodologyLink
      ui/                  DateRangePicker, SearchableSelect, Toggle, RangeSlider, FreshnessBadge, LanguageSwitcher
    utils/
      format.ts            Number/date formatting helpers
      colors.ts            Okabe-Ito categorical + YlGn sequential palettes
      plot-theme.ts        Observable Plot theme configuration
      map-style.ts         MapLibre GL style helpers
      filters.ts           Filter logic and URL state management
      time.ts              Time zone and date range utilities
  routes/
    +layout.svelte         Root layout with Header, Footer, locale
    +page.svelte           Home / overview dashboard
    estacoes/              Station explorer (list + [code] detail)
    analise/               Cross-metric analysis page
    historias/             Editorial data stories (list + [slug] detail)
    metodologia/           Methodology documentation page
    sobre/                 About page
    api/                   JSON API routes (stations, freshness, compare)
  hooks.server.ts          Server hooks (locale detection)
  app.css                  Design token system (Source Serif 4 + Inter, Okabe-Ito palette)
  app.html                 HTML shell
  app.d.ts                 SvelteKit type declarations
```

## Environment Variables

See `.env.example` for the full list.

| Variable | Scope | Required | Description |
|----------|-------|----------|-------------|
| `MOTHERDUCK_TOKEN` | Server | Yes | MotherDuck API token for Postgres wire protocol |
| `MOTHERDUCK_HOST` | Server | Yes | MotherDuck Postgres host (e.g., `pg.us-east-1-aws.motherduck.com`) |
| `MOTHERDUCK_DATABASE` | Server | Yes | MotherDuck database name |
| `PUBLIC_TILE_URL` | Public | No | MapLibre tile URL (default: OpenFreeMap Positron) |
| `PUBLIC_GITHUB_REPO` | Public | No | GitHub repo path for source links |
| `PUBLIC_MOTHERDUCK_SHARE` | Public | No | Public MotherDuck share URL for data access |

## Status

This package is a **skeleton** -- all components render placeholder data, all query modules return stub results, and all route load functions return typed placeholder objects. The structure, types, component tree, and test scaffolding are complete and ready for implementation.
