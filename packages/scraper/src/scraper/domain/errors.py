"""Custom exception hierarchy for the scraper."""


class GiraWatchError(Exception):
    """Base exception for all scraper errors."""


# --- API errors ---


class GiraApiError(GiraWatchError):
    """Base for GIRA API communication failures."""


class AuthError(GiraApiError):
    """JWT authentication failed. Scraper should abort immediately."""


class SchemaValidationError(GiraApiError):
    """API response doesn't match Pydantic schema. Indicates API drift."""


# --- Storage errors ---


class StorageError(GiraWatchError):
    """Base for storage backend failures."""


class StorageConnectionError(StorageError):
    """Cannot connect to storage backend. Raised on health_check() or connect."""


class WriteError(StorageError):
    """Write operation failed after connection established."""


# --- Other errors ---


class TransformError(GiraWatchError):
    """API-to-domain transformation failed (e.g., unknown enum value)."""


class AuditError(GiraWatchError):
    """Audit notification failed. Non-fatal -- data already written."""
