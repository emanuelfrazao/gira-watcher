"""CLI entrypoint: argparse, env vars, backend selection, scrape invocation."""

import argparse
import asyncio
import logging
import os
import sys
from datetime import UTC, datetime
from typing import NoReturn
from uuid import uuid4

import structlog

from scraper.api.client import GiraClient
from scraper.domain.enums import RunType
from scraper.domain.models import RunManifest
from scraper.orchestrator import ScrapeOrchestrator
from scraper.storage.local import LocalBackend
from scraper.storage.motherduck import MotherDuckBackend
from scraper.storage.protocol import StorageBackend

log = structlog.get_logger()


def _configure_logging() -> None:
    """Configure structlog: JSON in production, colored console in development."""
    env = os.environ.get("APP_ENV", "development")
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, level_name, logging.INFO)
    dev = env != "production"

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if dev:
        processors = [
            *shared_processors,
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        processors = [
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Suppress noisy httpx/httpcore stdlib loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


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

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        run_id=manifest.run_id,
        run_type=manifest.run_type.value,
    )
    log.info("scrape_run_started")

    backend.health_check()

    base_url = os.environ.get(
        "GIRA_API_BASE_URL", "https://c2g091p01.emel.pt/ws/graphql"
    )
    auth_url = os.environ.get(
        "GIRA_API_AUTH_URL", "https://c2g091p01.emel.pt/auth/login"
    )

    async with GiraClient(
        email=os.environ.get("GIRA_API_EMAIL"),
        password=os.environ.get("GIRA_API_PASSWORD"),
        base_url=base_url,
        auth_url=auth_url,
    ) as client:
        orchestrator = ScrapeOrchestrator(client=client, storage=backend)

        match run_type:
            case RunType.STATION:
                await orchestrator.run_station_scrape(manifest)
            case RunType.DETAIL:
                await orchestrator.run_detail_scrape(manifest)


def main(argv: list[str] | None = None) -> NoReturn:
    """Parse --run-type, read env vars, select backend, run scrape."""
    _configure_logging()
    args = _parse_args(argv)
    asyncio.run(_async_main(args))
    sys.exit(0)


if __name__ == "__main__":
    main()
