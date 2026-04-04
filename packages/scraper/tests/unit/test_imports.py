"""Group 1: Package structure -- importability and well-formedness."""

import importlib

import pytest


def test_import_top_level_package() -> None:
    """1.1: `import scraper` succeeds without error."""
    import scraper  # noqa: F401


@pytest.mark.parametrize(
    "subpackage",
    ["scraper.domain", "scraper.api", "scraper.storage"],
)
def test_import_subpackages(subpackage: str) -> None:
    """1.2: All subpackages are importable."""
    importlib.import_module(subpackage)


@pytest.mark.parametrize(
    "module",
    [
        "scraper.domain.enums",
        "scraper.domain.models",
        "scraper.domain.typed_dicts",
        "scraper.domain.errors",
        "scraper.api.schema",
        "scraper.api.client",
        "scraper.storage.protocol",
        "scraper.storage.motherduck",
        "scraper.storage.local",
        "scraper.storage.parquet",
        "scraper.orchestrator",
        "scraper.transform",
        "scraper.audit",
        "scraper.main",
    ],
)
def test_import_all_public_modules(module: str) -> None:
    """1.3 + 1.4: Every .py module is importable (no circular imports)."""
    importlib.import_module(module)


def test_py_typed_marker_exists() -> None:
    """1.5: `py.typed` marker exists in the package root."""
    import importlib.resources

    files = importlib.resources.files("scraper")
    py_typed = files.joinpath("py.typed")
    assert py_typed.is_file()  # type: ignore[union-attr]
