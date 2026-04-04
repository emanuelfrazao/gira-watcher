"""Group 4: Domain errors -- hierarchy catchability."""

import pytest

from scraper.domain.errors import (
    AuditError,
    AuthError,
    GiraApiError,
    GiraWatchError,
    SchemaValidationError,
    StorageConnectionError,
    StorageError,
    TransformError,
    WriteError,
)


@pytest.mark.parametrize(
    "error_class",
    [
        GiraApiError,
        AuthError,
        SchemaValidationError,
        StorageError,
        StorageConnectionError,
        WriteError,
        TransformError,
        AuditError,
    ],
    ids=lambda cls: cls.__name__,
)
def test_all_errors_are_gira_watch_errors(error_class: type[GiraWatchError]) -> None:
    """4.1: All error classes are subclasses of GiraWatchError."""
    assert issubclass(error_class, GiraWatchError)


def test_base_error_is_catchable() -> None:
    """4.2: `raise GiraApiError(...)` is caught by `except GiraWatchError`."""
    with pytest.raises(GiraWatchError):
        raise GiraApiError("test error")


def test_errors_carry_messages() -> None:
    """4.3: Each error class accepts a message string and str() returns it."""
    msg = "something went wrong"
    for error_class in [
        GiraWatchError,
        GiraApiError,
        AuthError,
        SchemaValidationError,
        StorageError,
        StorageConnectionError,
        WriteError,
        TransformError,
        AuditError,
    ]:
        err = error_class(msg)
        assert str(err) == msg
