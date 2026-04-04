"""Scrape orchestrator: wires API client, transform functions, and storage backend."""

from scraper.api.client import GiraClient
from scraper.domain.models import RunManifest, WriteResult
from scraper.storage.protocol import StorageBackend


class ScrapeOrchestrator:
    """Wires API client, transform functions, and storage backend."""

    def __init__(
        self,
        client: GiraClient,
        storage: StorageBackend,
        max_concurrency: int = 15,
    ) -> None:
        self._client = client
        self._storage = storage
        self._max_concurrency = max_concurrency

    async def run_station_scrape(self, manifest: RunManifest) -> WriteResult:
        """Execute a station-level scrape run."""
        raise NotImplementedError

    async def run_detail_scrape(self, manifest: RunManifest) -> WriteResult:
        """Execute a detail-level scrape run (docks + bikes per station)."""
        raise NotImplementedError
