# Legal and Ethical Considerations

> **Disclaimer:** This document is a lay analysis of the relevant legal and ethical considerations. It is not legal advice and should not be relied upon as such.

## API Access

### Station-level data (unauthenticated)

The GIRA station status API (`getStations`) is the same endpoint used by GIRA's own official mobile application. It requires no authentication, no API key, and no account. It is, by technical definition, a public endpoint. Third-party applications (notably GIRA+) query the same API without objection from the operator.

Querying a public, unauthenticated API is standard practice in data journalism and civic technology. The project makes no attempt to circumvent any access control, reverse-engineer proprietary protocols, or access any administrative interface.

All five pre-registered metrics in [`METHODOLOGY.md`](METHODOLOGY.md) are powered exclusively by this unauthenticated endpoint.

### Dock and bike detail data (authenticated)

During project investigation, it was discovered that the dock-level (`getDocks`) and bike-level (`getBikes`) API endpoints require JWT authentication -- they are not publicly accessible without a login.

GIRA Watch accesses these endpoints using the project maintainer's own legitimate GIRA account credentials. This is analogous to a journalist logging into a public-facing service with their own account to access information available to any registered user. Specifically:

- **No credentials are bypassed, stolen, or shared.** The maintainer uses their own GIRA account.
- **No terms of service are circumvented.** The GIRA app does not publish terms restricting automated access to the user-facing API.
- **The data returned is operational infrastructure data** (dock state, bike position, battery level), not personal or user-specific data.
- **The authenticated endpoints are supplementary.** All core metrics use the unauthenticated station-level endpoint. Dock/bike detail data enriches analysis but is not required.

## Rate Limiting and Responsible Scraping

The scraper runs at a fixed cadence of **one batch request per 5 minutes** covering all stations. Within each batch, requests are made sequentially with brief delays between calls. This produces a very low request rate compared to normal user traffic from the mobile application.

The scraper does not:
- Attempt to circumvent any rate limiting or anti-scraping measures
- Make concurrent or parallel requests to the API
- Retry aggressively on failure (a failed run is recorded and the next scheduled run proceeds normally)
- Query more frequently than the minimum useful interval for the analytical goals

## Data Minimisation

Only station-level operational data is collected: station identifiers, coordinates, dock/bike counts, and timestamps. At the detail tier: dock state (empty/occupied) and bike battery level.

**No personal data is collected or stored:**
- No user accounts, trip data, or session data
- No personally identifiable information of any kind
- No tracking of individual users or their movements

The project is fully aligned with data minimisation principles under GDPR Article 5(1)(c), as all collected data pertains entirely to public transport infrastructure, not to individuals.

## Public Interest Justification

GIRA operates as a public concession in Lisbon -- a service contracted by the city government, funded in part by public money, and intended to serve the public. The operational performance of a public concession is a matter of direct public interest.

The journalistic purpose of GIRA Watch -- providing citizens, journalists, and municipal authorities with objective, systematic evidence of service quality -- constitutes legitimate public interest activity. This is consistent with:

- **Press freedom and data journalism:** Monitoring public services using publicly available data is a core function of journalism and civic oversight.
- **Right to information:** Citizens have a legitimate interest in knowing whether public concession obligations are being met.
- **Precedent:** Numerous civic technology projects worldwide monitor public transit systems using similar methods (e.g., transit data scrapers for bus/metro reliability analysis).

## Summary

| Consideration | Status |
|---------------|--------|
| Station-level API access | Unauthenticated public endpoint, same as GIRA mobile app |
| Dock/bike detail API access | Maintainer's own legitimate GIRA account |
| Rate limiting | One batch per 5 minutes, sequential, with delays |
| Personal data | None collected or stored |
| GDPR compliance | Infrastructure data only, data minimisation satisfied |
| Public interest | Public concession monitoring, journalistic purpose |
