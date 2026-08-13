"""Release coordination helpers (P2 scope).

Idempotent release actions: detect "already published" rather than create
duplicates; require clean/locked state and human approval.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ReleaseCandidate:
    asset: str
    version: str
    lock_path: Path
    approvals: list[str] = field(default_factory=list)
    published: bool = False


def load_release_state(state_path: Path) -> dict[str, Any]:
    if not state_path.is_file():
        return {"releases": []}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"releases": []}


def already_published(state: dict[str, Any], asset: str, version: str) -> bool:
    for rel in state.get("releases", []):
        if rel.get("asset") == asset and rel.get("version") == version:
            return True
    return False


def mark_published(state_path: Path, asset: str, version: str, run_id: str) -> None:
    """Idempotently record a published release (mutex should be held by caller)."""
    state = load_release_state(state_path)
    if already_published(state, asset, version):
        return
    state["releases"].append(
        {"asset": asset, "version": version, "run_id": run_id}
    )
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
