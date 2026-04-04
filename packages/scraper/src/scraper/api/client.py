"""Async HTTP client for the GIRA API."""

import httpx

from scraper.api.schema import ApiBike, ApiDock, ApiStation


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
        auth_url: str = "https://c2g091p01.emel.pt/auth",
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
        self._http_client = httpx.AsyncClient(timeout=self._timeout)
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
