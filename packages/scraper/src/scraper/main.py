"""CLI entrypoint: argparse, env vars, backend selection, scrape invocation."""

import argparse
import asyncio
import os
import sys
from datetime import UTC, datetime
from typing import NoReturn
from uuid import uuid4

from scraper.api.client import GiraClient
from scraper.domain.enums import RunType
from scraper.domain.models import RunManifest
from scraper.orchestrator import ScrapeOrchestrator
from scraper.storage.local import LocalBackend
from scraper.storage.motherduck import MotherDuckBackend
from scraper.storage.protocol import StorageBackend


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="scraper",
        description="GIRA bicycle station data scraper",
    )
    parser.add_argument(
        "--run-type",
        choices=["station", "detail"],
        required=True,
        help="Type of scrape run to execute",
    )
    return parser.parse_args(argv)


def _select_backend() -> StorageBackend:
    """Select storage backend from environment variables."""
    storage_url = os.environ.get("GIRA_STORAGE_URL", "")
    storage_token = os.environ.get("GIRA_STORAGE_TOKEN")

    if storage_token is not None:
        return MotherDuckBackend(connection_url=storage_url, token=storage_token)
    return LocalBackend(db_path=storage_url)


def _build_manifest(run_type: RunType) -> RunManifest:
    """Build a RunManifest from environment variables."""
    return RunManifest(
        run_id=str(uuid4()),
        run_type=run_type,
        commit_sha=os.environ.get("GIRA_COMMIT_SHA", "unknown"),
        github_run_url=os.environ.get("GITHUB_RUN_URL"),
        started_at=datetime.now(UTC),
        scheduler_identity=os.environ.get("GIRA_SCHEDULER_IDENTITY", "local-dev"),
    )


async def _async_main(args: argparse.Namespace) -> None:
    """Async entrypoint."""
    run_type = RunType(args.run_type)
    backend = _select_backend()
    manifest = _build_manifest(run_type)

    backend.health_check()

    async with GiraClient(
        email=os.environ.get("GIRA_API_EMAIL"),
        password=os.environ.get("GIRA_API_PASSWORD"),
    ) as client:
        orchestrator = ScrapeOrchestrator(client=client, storage=backend)

        match run_type:
            case RunType.STATION:
                await orchestrator.run_station_scrape(manifest)
            case RunType.DETAIL:
                await orchestrator.run_detail_scrape(manifest)


def main(argv: list[str] | None = None) -> NoReturn:
    """Parse --run-type, read env vars, select backend, run scrape."""
    args = _parse_args(argv)
    asyncio.run(_async_main(args))
    sys.exit(0)


if __name__ == "__main__":
    main()
