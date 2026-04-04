"""Auto-apply integration marker to all tests in this directory."""

import pathlib

import pytest

_INTEGRATION_DIR = pathlib.Path(__file__).parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Add 'integration' marker to all tests under the integration/ directory."""
    for item in items:
        if _INTEGRATION_DIR in pathlib.Path(item.fspath).parents:
            item.add_marker(pytest.mark.integration)
