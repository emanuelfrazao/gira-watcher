"""Async HTTP client for the GIRA API."""

import time
from importlib.metadata import PackageNotFoundError, version

import httpx
import structlog

from scraper.api.schema import ApiBike, ApiDock, ApiStation

log = structlog.get_logger()


def _get_version() -> str:
    """Read package version from installed metadata."""
    try:
        return version("gira-scraper")
    except PackageNotFoundError:
        return "dev"


async def _log_request(request: httpx.Request) -> None:
    """Log outgoing HTTP request and stash start time for elapsed calculation."""
    request.extensions["start_time"] = time.monotonic()
    log.debug(
        "http_request",
        method=request.method,
        url=str(request.url),
    )


async def _log_response(response: httpx.Response) -> None:
    """Log HTTP response with status code and elapsed time."""
    request = response.request
    start = request.extensions.get("start_time")
    elapsed_ms = round((time.monotonic() - start) * 1000, 1) if start else None
    log.debug(
        "http_response",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        elapsed_ms=elapsed_ms,
    )


class GiraClient:
    """Async HTTP client for GIRA API. Manages httpx lifecycle and lazy JWT.

    Usage::

        async with GiraClient(email=..., password=...) as client:
            stations = await client.get_stations()
    """

    def __init__(
        self,
        email: str | None = None,
        password: str | None = None,
        base_url: str = "https://c2g091p01.emel.pt/ws/graphql",
        auth_url: str = "https://c2g091p01.emel.pt/auth/login",
        timeout: float = 15.0,
    ) -> None:
        self._email = email
        self._password = password
        self._base_url = base_url
        self._auth_url = auth_url
        self._timeout = timeout
        self._http_client: httpx.AsyncClient | None = None
        self._token: str | None = None

    async def __aenter__(self) -> "GiraClient":
        user_agent = (
            f"gira-watcher/{_get_version()} "
            "(+https://github.com/emanueelfrazao/gira-watcher)"
        )
        self._http_client = httpx.AsyncClient(
            timeout=self._timeout,
            headers={"User-Agent": user_agent},
            event_hooks={"request": [_log_request], "response": [_log_response]},
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    async def get_stations(self) -> list[ApiStation]:
        """Fetch all stations from the GIRA API."""
        raise NotImplementedError

    async def get_docks(self, station_serial: str) -> list[ApiDock]:
        """Fetch docks for a station by its serial number."""
        raise NotImplementedError

    async def get_bikes(self, station_serial: str) -> list[ApiBike]:
        """Fetch bikes for a station by its serial number."""
        raise NotImplementedError
