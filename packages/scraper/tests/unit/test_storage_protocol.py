"""Group 6: Storage Protocol compliance -- all backends satisfy the Protocol."""

import pytest

from scraper.storage.local import LocalBackend
from scraper.storage.motherduck import MotherDuckBackend
from scraper.storage.parquet import ParquetBackend
from scraper.storage.protocol import StorageBackend


@pytest.mark.parametrize(
    "backend_class",
    [MotherDuckBackend, LocalBackend, ParquetBackend],
    ids=["MotherDuckBackend", "LocalBackend", "ParquetBackend"],
)
def test_backend_satisfies_protocol(backend_class: type[object]) -> None:
    """6.1-6.3: Each backend is a structural subtype of StorageBackend."""
    assert issubclass(backend_class, StorageBackend)


@pytest.mark.parametrize(
    "backend_class",
    [MotherDuckBackend, LocalBackend, ParquetBackend],
    ids=["MotherDuckBackend", "LocalBackend", "ParquetBackend"],
)
def test_backend_has_all_protocol_methods(backend_class: type[object]) -> None:
    """6.4: All Protocol methods exist as callable attributes."""
    for method_name in ["health_check", "run"]:
        assert hasattr(backend_class, method_name)
        assert callable(getattr(backend_class, method_name))
