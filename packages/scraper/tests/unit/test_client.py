"""Group 9: GiraClient instantiation and method existence."""

import inspect

from scraper.api.client import GiraClient


def test_gira_client_instantiates() -> None:
    """9.1: GiraClient constructor does not raise."""
    client = GiraClient()
    assert client is not None


def test_gira_client_has_expected_async_methods() -> None:
    """9.2: get_stations, get_docks, get_bikes are coroutine functions."""
    client = GiraClient()
    for method_name in ["get_stations", "get_docks", "get_bikes"]:
        method = getattr(client, method_name)
        assert inspect.iscoroutinefunction(method), f"{method_name} is not a coroutine function"
