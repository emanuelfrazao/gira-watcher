"""Auto-apply unit marker to all tests in this directory."""

import pathlib

import pytest

_UNIT_DIR = pathlib.Path(__file__).parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Add 'unit' marker to all tests under the unit/ directory."""
    for item in items:
        if _UNIT_DIR in pathlib.Path(item.fspath).parents:
            item.add_marker(pytest.mark.unit)
