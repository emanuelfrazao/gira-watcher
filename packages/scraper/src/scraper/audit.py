"""Audit trail: repository_dispatch notification to audit repo."""

from scraper.domain.models import RunManifest, WriteResult


async def notify_audit_repo(
    manifest: RunManifest,
    result: WriteResult,
    audit_token: str | None,
    audit_repo: str | None,
) -> None:
    """Send repository_dispatch to audit repo. No-op if token/repo is None."""
    if audit_token is None or audit_repo is None:
        return
    raise NotImplementedError
