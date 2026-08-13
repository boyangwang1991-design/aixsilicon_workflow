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
    state["releases"].append({"asset": asset, "version": version, "run_id": run_id})
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def build_release_material(
    *,
    asset: str,
    version: str,
    manifest: Any,
    profile: str,
    override: Any,
    root: Path,
) -> dict[str, Any]:
    """Collect clean/locked state and generate release material (YAML manifest).

    Enforces the G7 release guard (dirty/override blocked) before staging
    (plan.md §23 / §24 G7; release guard lives in workspace.release_guard_ok).
    """
    from aixworkflow.workspace import release_guard_ok

    guard = release_guard_ok(manifest, root, override, require_clean=True)
    if not guard.ok:
        from aixworkflow.errors import BlockedError

        raise BlockedError(f"release material blocked: {guard.reason}")

    repos: dict[str, dict[str, str]] = {}
    try:
        selected = manifest.profile(profile)
        for repo in manifest.enabled_repositories(selected):
            repos[repo.id] = {
                "url": repo.remote_url(manifest.remotes),
                "branch": repo.revision.get("branch", ""),
                "path": repo.path,
            }
    except Exception:  # noqa: BLE001 - best-effort repo summary
        pass

    lines = [
        "schema_version: aix.release-manifest/v1",
        f"asset: {asset}",
        f"version: {version}",
        f"profile: {profile}",
        "repositories:",
    ]
    for rid, info in repos.items():
        lines.append(f"  {rid}:")
        lines.append(f"    url: {info['url']}")
        lines.append(f"    branch: {info['branch']}")
        lines.append(f"    path: {info['path']}")
    lines.append("gate: G7-PENDING-APPROVAL")
    manifest_yaml = "\n".join(lines) + "\n"

    return {
        "asset": asset,
        "version": version,
        "profile": profile,
        "repositories": repos,
        "manifest_yaml": manifest_yaml,
    }
