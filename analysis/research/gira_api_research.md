# GIRA Internal API — Endpoints, Schemas, and Reverse-Engineering Findings

> Part of research: GIRA (Lisbon) bicycle station availability monitoring

## Summary

The GIRA bike-sharing system (operated by EMEL, Lisbon's municipal mobility company) exposes an undocumented GraphQL API used by the official mobile apps. Multiple independent developers have reverse-engineered this API and published working alternative clients. The API base URL is `https://c2g091p01.emel.pt`, with a REST auth endpoint and a GraphQL endpoint. Station availability (bikes and docks per station) is available both via authenticated GraphQL queries and via real-time WebSocket subscriptions. EMEL also provides a separate open-data platform with static station files, but that data updates at most daily and is less useful for live monitoring. The core scraping-relevant endpoints (unauthenticated station list, real-time dock/bike counts) require authentication via JWT access tokens obtained from a Firebase-based login flow.

---

## Findings

### 1. API Base URLs and Endpoints

Three domains are used by the GIRA ecosystem [1, 2]:

| Host | Role |
|------|------|
| `https://c2g091p01.emel.pt/auth` | Authentication — obtains access/refresh tokens |
| `https://c2g091p01.emel.pt/api/graphql` | Main GraphQL API (HTTP) |
| `wss://c2g091p01.emel.pt/ws/graphql` | Real-time GraphQL subscriptions (WebSocket) |

The proxy whitelist in `mGira` also references `api-auth.emel.pt` and `apigira.emel.pt` as historical/alternative authentication and API domains [1], but the gira-mais project (the more recent and detailed reverse-engineering effort) confirms `c2g091p01.emel.pt` as the current backend host [2].

EMEL additionally operates a public open-data platform:
- `https://dados.emel.pt` — static file downloads (CSV/JSON/XML) for station metadata, updated up to every 24 hours [3, 4]
- `https://opendata.emel.pt` — successor portal (the older `emel.city-platform.com/opendata/` now redirects to a security notice)

### 2. Authentication Flow

All GraphQL API calls require a `Bearer` token in the `Authorization` header [2]. The authentication sequence is:

1. **Login**: POST credentials (email + password) to the auth endpoint; receives `accessToken` and `refreshToken`.
2. **Firebase token**: A separate call to obtain a Firebase device-verification token (`x-firebase-token`), which is required alongside the Bearer token for some operations (notably WebSocket subscriptions and the `validateLogin` mutation).
3. **Token refresh**: The access token is a JWT; its expiration is read from the `exp` claim. A refresh call fires 30 seconds before expiry (5 retries, 2000 ms apart). Falls back to re-login if refresh fails.

Request headers used by the gira-mais client [2]:

```
User-Agent: Gira/3.4.3 (Android 34)
Content-Type: application/json
Authorization: Bearer <accessToken>
x-firebase-token: <firebaseToken>   # only for some operations
```

The mGira (older) project adds the following in its proxy layer [1]:

```
X-Authorization: <value>  →  forwarded as  Authorization: <value>
```

### 3. GraphQL Queries — Station Availability

The primary queries for station availability data [2]:

**List all stations (summary counts):**
```graphql
query getStations {
  getStations {
    code
    description
    latitude
    longitude
    name
    bikes
    docks
    serialNumber
    assetStatus
  }
}
```
Returns one record per station with integer `bikes` (available bikes) and `docks` (available empty docks).

**Per-station detail — bikes at a station:**
```graphql
query {
  getBikes(input: "<stationId>") {
    battery
    code
    name
    kms
    serialNumber
    type
    parent
  }
}
```

**Per-station detail — dock states:**
```graphql
query {
  getDocks(input: "<stationId>") {
    ledStatus
    lockStatus
    serialNumber
    code
    name
  }
}
```

**Active trip (per authenticated user):**
```graphql
query {
  activeTrip {
    user, startDate, endDate, startLocation, endLocation,
    distance, rating, photo, cost, startOccupation, endOccupation,
    totalBonus, client, costBonus, comment, compensationTime,
    endTripDock, tripStatus, code, name, description,
    creationDate, createdBy, updateDate, updatedBy, defaultOrder, version
  }
}
```

**Trip history (paginated):**
```graphql
query ($input: PageInput) {
  tripHistory(pageInput: $input) {
    code, startDate, endDate, rating, bikeName,
    startLocation, endLocation, bonus, usedPoints, cost, bikeType
  }
}
```

### 4. GraphQL Mutations

The full SDL schema (recovered from gira-mais source) defines 27 mutations [2, 5]:

| Mutation | Purpose |
|----------|---------|
| `startTrip` | Begin a bike rental |
| `rateTrip` | Submit rating after trip |
| `reserveBike` | Reserve a bike at a station |
| `cancelBikeReserve` | Cancel an existing reservation |
| `validateLogin` | Confirm device session with Firebase token |
| `registerClient` | Create a new user account |
| `deleteClient` | Remove account |
| `creditCardTopUp` | Add credit via card |
| `subscriptionEasyPay` / `subscriptionTopUpPayPal` | Subscribe/renew |
| `insertPromotionalCode` | Redeem promo code |
| `emailInvoices` | Request invoice by email |

### 5. Real-Time WebSocket Subscriptions

The WebSocket endpoint (`wss://c2g091p01.emel.pt/ws/graphql`) uses the `graphql-ws` subprotocol [2, 6]. Connection initialization sends:

```json
{ "type": "connection_init", "payload": { "headers": { "Authorization": "Bearer <token>", "x-firebase-token": "<firebaseToken>" } } }
```

Two key subscriptions for station monitoring:

**Operational stations (live availability):**
```graphql
subscription {
  operationalStationsSubscription {
    code
    name
    latitude
    longitude
    bikes
    docks
    serialNumber
    assetStatus
    assetCondition
    assetType
  }
}
```

**Active trip cost (per-user, real-time):**
```graphql
subscription {
  activeTripSubscription {
    # bike, cost, points, trip state fields
  }
}
```

Reconnection uses exponential backoff (+1000 ms per attempt).

### 6. Response Schema — Key Types

Recovered from `api-types.ts` in gira-mais [2]:

**StationInfo:**
- `code` (string), `name` (string), `description` (string)
- `serialNumber` (string), `zone` (string?)
- `latitude` (float), `longitude` (float)
- `assetType` (enum: "Station"), `assetStatus` (enum: "Active" | "Repair"), `assetCondition` (enum: "New")
- `bikes` (int — available bikes), `docks` (int — available empty docks)
- `dockList` (array of `Dock`)
- Audit fields: `creationDate`, `createdBy`, `updateDate`, `updatedBy`, `version`

**Dock:**
- `code`, `name`, `serialNumber`
- `ledStatus` (string), `lockStatus` (string)
- `assetType`, `assetStatus`, `assetCondition`
- `latitude`, `longitude`

**Bike:**
- `code`, `name`, `serialNumber`
- `type` (enum: "A" or "B" — likely regular vs e-bike), `kms` (float), `battery` (int)
- `assetStatus`, `assetCondition`
- `parent` (station code)

**Fleet size**: The bikeMapping file in gira-mais contains over 2,300 individual bike ID-to-serial-number entries (E-series IDs E0001–E2336+, plus some C-series) [7].

### 7. Public Open Data (Static)

EMEL provides static station data via `dados.emel.pt` [3, 4]:

- JSON: `https://dados.emel.pt/dataset/57181518-0708-4fb5-a7d1-69875dee8478/resource/d1950d9d-26be-4ced-b1c4-9af65c8d2c70/download/girastations.json`
- CSV: `https://dados.emel.pt/dataset/57181518-0708-4fb5-a7d1-69875dee8478/resource/2cdce96f-6efd-4734-baf8-0d48984b19e0/download/girastations.csv`
- XML (DATEX II): `https://dados.emel.pt/dataset/57181518-0708-4fb5-a7d1-69875dee8478/resource/a0064fee-a75e-417b-a2e7-4649b3b6882f/download/girastations.xml`

These are licensed under CC BY-SA and updated up to every 24 hours. Field content includes geographic location, operating hours, pricing, payment methods, and WiFi availability — but **not real-time bike/dock counts**. The historical dataset (`dados.gov.pt`) covers 2020–2023 Q1 in XLSX/7z/ZIP format [8].

### 8. Known Alternative Client Projects

Three open-source projects have successfully reverse-engineered and used the GIRA API:

| Project | Tech stack | Notes |
|---------|-----------|-------|
| **mGira** (`afonsosousah/mGira`) | JavaScript, PHP proxy | First public alternative client; uses a PHP CORS proxy to relay API calls; documented in RTP news article [1, 9] |
| **gira-mais** (`rt-evil-inc/gira-mais`) | SvelteKit + Capacitor (Android/iOS) | Most detailed source; exposes full SDL schema, type definitions, and constants [2, 6, 7] |
| **pybikes** (`eskerda/pybikes`) | Python | General bike-share scraping library; GIRA may be supported as a network [10] |

EMEL's official response to mGira was that the access "arose from EMEL's need for technological evolution based on a growing culture of interoperability, transparency and innovation" — a de facto endorsement, though without formal API documentation [9]. The GitHub issue thread on gira-mais also references EU Directive 2019/1024 and Portuguese Law 68/2021 as legal bases for open mobility data access [11].

### 9. Authentication Requirements per Endpoint

| Endpoint | Auth required? |
|----------|---------------|
| `getStations` (station list with bike/dock counts) | Yes — Bearer token |
| `getBikes(stationId)` / `getDocks(stationId)` | Yes — Bearer token |
| `operationalStationsSubscription` (WebSocket) | Yes — Bearer token + Firebase token |
| `dados.emel.pt` static downloads | No (public) |
| `dados.gov.pt` historical archives | No (public) |

---

## Key Takeaways

- The canonical internal API base URL is `https://c2g091p01.emel.pt`, with `/auth`, `/api/graphql`, and `/ws/graphql` paths.
- The API is GraphQL-only (no REST endpoints for live data). Authentication uses Bearer JWTs obtained from the EMEL auth endpoint, supplemented by Firebase tokens for WebSocket subscriptions.
- The `getStations` query returns `bikes` and `docks` integer counts per station in a single call — the most efficient endpoint for availability monitoring.
- EMEL has tacitly accepted third-party use of this API; it is not publicly documented but has not been blocked.
- The real-time WebSocket subscription (`operationalStationsSubscription`) provides push-based updates without polling.
- Static open data (station metadata) is freely available without auth, but does not include live availability.
- Bike type is encoded as `"A"` or `"B"` in the `Stype` enum, likely distinguishing regular from electric bikes.

---

## Gaps and Limitations

- The exact authentication endpoint path on `c2g091p01.emel.pt/auth` (e.g., `/auth/token`, `/auth/login`) is not confirmed — only the base auth URL is extractable from constants.ts without running the code.
- The `validateLogin` mutation requires a Firebase token; the process for obtaining this token (Firebase project ID, app credentials) is not fully documented in the open-source projects reviewed.
- It is unclear whether `getStations` returns all stations in a single response or requires pagination. The schema shows a `PageInput` type for trip history but stations appear to be returned in bulk.
- The distinction between `assetStatus: "Active"` / `"Repair"` and the `docks` count is not fully documented — a station marked "Repair" may still appear in the list with zero bikes.
- The `c2g091p01.emel.pt` hostname suggests an internal/staging server address; whether this is stable for production scraping is unconfirmed.
- EMEL has not published an SLA, rate-limit policy, or terms of service for third-party API access.

---

## References

1. afonsosousah — [mGira: Uma melhor aplicação para o sistema de bicicletas partilhadas GIRA](https://github.com/afonsosousah/mGira) — 2023
2. rt-evil-inc — [gira-mais: Aplicação alternativa para o sistema de bicicletas partilhadas de Lisboa](https://github.com/rt-evil-inc/gira-mais) — 2024
3. EMEL — [Estações GIRA dataset (JSON/CSV/XML)](https://dados.emel.pt/dataset/girastations) — Updated 2026-04-04
4. dados.gov.pt — [Estações GIRA – Portal Dados Abertos](https://dados.gov.pt/en/datasets/gira-bicicletas-de-lisboa-1/) — accessed 2026-04-04
5. rt-evil-inc — [sdl.gql — Full GraphQL schema](https://github.com/rt-evil-inc/gira-mais/blob/main/src/lib/sdl.gql) — 2024
6. rt-evil-inc — [ws.ts — WebSocket subscription implementation](https://github.com/rt-evil-inc/gira-mais/blob/main/src/lib/gira-api/ws.ts) — 2024
7. rt-evil-inc — [bikeMapping.ts — Fleet ID-to-serial mapping (2300+ bikes)](https://github.com/rt-evil-inc/gira-mais/blob/main/src/lib/gira-api/bikeMapping.ts) — 2024
8. EMEL / dados.gov.pt — [GIRA - Bicicletas de Lisboa (Histórico)](https://dados.gov.pt/en/datasets/gira-bicicletas-de-lisboa-historico/) — data through 2023
9. RTP Notícias — [Bicicletas em Lisboa. Jovem programou alternativa para escapar aos problemas da aplicação Gira](https://www.rtp.pt/noticias/pais/bicicletas-em-lisboa-jovem-programou-alternativa-para-escapar-aos-problemas-da-aplicacao-gira_n1538912) — Dec 2023
10. eskerda — [pybikes: bike sharing + python](https://github.com/eskerda/pybikes) — ongoing
11. rt-evil-inc — [Autorização? — GitHub Issue #2, gira-mais](https://github.com/rt-evil-inc/gira-mais/issues/2) — 2024
