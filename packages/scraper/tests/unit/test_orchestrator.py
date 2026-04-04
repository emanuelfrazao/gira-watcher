"""Group 10: Orchestrator and transform stubs."""

import inspect
from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from scraper.api.client import GiraClient
from scraper.domain.enums import RunType
from scraper.domain.models import RunManifest
from scraper.orchestrator import ScrapeOrchestrator
from scraper.transform import (
    extract_bike_dims,
    extract_bike_snapshots,
    extract_dock_dims,
    extract_dock_snapshots,
    extract_station_dims,
    extract_station_snapshots,
)


def test_scrape_orchestrator_instantiates() -> None:
    """10.1: ScrapeOrchestrator accepts client, storage, max_concurrency."""
    client = GiraClient()
    storage = MagicMock()
    orchestrator = ScrapeOrchestrator(client=client, storage=storage, max_concurrency=10)
    assert orchestrator is not None


@pytest.mark.asyncio
async def test_run_station_scrape_raises_not_implemented() -> None:
    """10.2: run_station_scrape raises NotImplementedError."""
    client = GiraClient()
    storage = MagicMock()
    orchestrator = ScrapeOrchestrator(client=client, storage=storage)
    manifest = RunManifest(
        run_id="test",
        run_type=RunType.STATION,
        commit_sha="abc",
        github_run_url=None,
        started_at=datetime.now(UTC),
        scheduler_identity="test",
    )
    with pytest.raises(NotImplementedError):
        await orchestrator.run_station_scrape(manifest)


@pytest.mark.asyncio
async def test_run_detail_scrape_raises_not_implemented() -> None:
    """10.3: run_detail_scrape raises NotImplementedError."""
    client = GiraClient()
    storage = MagicMock()
    orchestrator = ScrapeOrchestrator(client=client, storage=storage)
    manifest = RunManifest(
        run_id="test",
        run_type=RunType.DETAIL,
        commit_sha="abc",
        github_run_url=None,
        started_at=datetime.now(UTC),
        scheduler_identity="test",
    )
    with pytest.raises(NotImplementedError):
        await orchestrator.run_detail_scrape(manifest)


@pytest.mark.parametrize(
    "func",
    [
        extract_station_dims,
        extract_station_snapshots,
        extract_dock_dims,
        extract_dock_snapshots,
        extract_bike_dims,
        extract_bike_snapshots,
    ],
    ids=[
        "extract_station_dims",
        "extract_station_snapshots",
        "extract_dock_dims",
        "extract_dock_snapshots",
        "extract_bike_dims",
        "extract_bike_snapshots",
    ],
)
def test_transform_functions_exist(func: object) -> None:
    """10.4: All transform functions are importable callables."""
    assert callable(func)
    assert not inspect.iscoroutinefunction(func)
