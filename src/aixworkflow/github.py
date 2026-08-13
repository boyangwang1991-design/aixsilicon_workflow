"""GitHub integration helpers (P2 scope).

Coordinates cross-repo CI: workflow_dispatch, repository_dispatch, Change
Bundle PR head checkout, and event-loop guard with correlation_id/depth.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass
class DispatchEvent:
    correlation_id: str
    source_repo: str
    source_sha: str
    depth: int = 0

    def to_payload(self) -> dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "source_repo": self.source_repo,
            "source_sha": self.source_sha,
            "depth": self.depth,
        }


MAX_EVENT_DEPTH = 3


def token() -> str | None:
    """Return the short-lived CI token, or None when not configured."""
    return os.environ.get("AIX_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")


def guard_event_loop(event: DispatchEvent) -> None:
    """Refuse recursive events beyond the allowed depth (event-loop guard)."""
    from aixworkflow.errors import BlockedError

    if event.depth > MAX_EVENT_DEPTH:
        raise BlockedError(
            f"refusing cross-repo event at depth {event.depth} (max {MAX_EVENT_DEPTH})"
        )
