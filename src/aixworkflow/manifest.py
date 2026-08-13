"""Manifest loading: extends resolution, deep merge, schema validation, overrides."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aixworkflow.errors import ManifestError
from aixworkflow.models import Manifest, Profile, Repository, WorkspaceSpec
from aixworkflow.schema import validate
from aixworkflow.yamlutil import deep_merge, load_yaml

OVERRIDE_SCHEMA_VERSION = "aix.workspace-override/v1"


@dataclass
class Override:
    """Local override document (overrides/local.yaml)."""

    source_path: Path | None
    repositories: dict[str, dict[str, Any]] = field(default_factory=dict)

    def revision_for(self, repo_id: str) -> dict[str, str] | None:
        entry = self.repositories.get(repo_id)
        if not entry:
            return None
        rev = entry.get("revision")
        if not isinstance(rev, dict):
            return None
        return {str(k): str(v) for k, v in rev.items()}


def _load_with_extends(
    path: Path,
    visited: set[Path],
    base_dir: Path,
) -> dict[str, Any]:
    """Load a manifest document, resolving its `extends` chain."""
    resolved = path.resolve()
    if resolved in visited:
        raise ManifestError(f"manifest extends cycle detected at {path}")
    visited.add(resolved)

    doc = load_yaml(path)
    extends = doc.get("extends")
    if extends:
        base_path = (path.parent / str(extends)).resolve()
        if not base_path.is_file():
            raise ManifestError(f"manifest '{path}' extends missing file: {base_path}")
        base_doc = _load_with_extends(base_path, visited, base_dir)
        merged = deep_merge(base_doc, doc)
        # repositories merge by id so child entries can override base entries
        merged["repositories"] = _merge_repositories(base_doc, doc)
    else:
        merged = doc

    # strip the extends key from the merged document
    merged.pop("extends", None)
    return merged


def _merge_repositories(base: dict[str, Any], child: dict[str, Any]) -> list[dict[str, Any]]:
    base_repos: list[dict[str, Any]] = list(base.get("repositories", []))
    child_repos: list[dict[str, Any]] = list(child.get("repositories", []))
    if not child_repos:
        return base_repos
    by_id = {str(r["id"]): r for r in base_repos}
    for repo in child_repos:
        by_id[str(repo["id"])] = repo
    # preserve original base ordering
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for repo in base_repos:
        rid = str(repo["id"])
        if rid not in seen:
            result.append(by_id[rid])
            seen.add(rid)
    for repo in child_repos:
        rid = str(repo["id"])
        if rid not in seen:
            result.append(by_id[rid])
            seen.add(rid)
    return result


def load_manifest(
    path: Path,
    *,
    profile_name: str | None = None,
    override_path: Path | None = None,
) -> tuple[Manifest, str, Override]:
    """Load and validate a workspace manifest.

    Returns (manifest, selected_profile_name, override).
    """
    if not path.is_file():
        raise ManifestError(f"manifest not found: {path}")

    doc = _load_with_extends(path, set(), path.parent)
    validate(doc, "manifest", source=str(path))

    workspace = WorkspaceSpec.from_dict(doc.get("workspace", {}))
    remotes: dict[str, dict[str, str]] = {
        str(k): {str(kk): str(vv) for kk, vv in v.items()}
        for k, v in doc.get("remotes", {}).items()
    }
    repositories = [Repository.from_dict(r) for r in doc.get("repositories", [])]
    profiles = {
        str(k): Profile(
            name=str(k), include_groups=tuple(str(g) for g in v.get("include_groups", []))
        )
        for k, v in doc.get("profiles", {}).items()
    }

    manifest = Manifest(
        source_path=path,
        workspace=workspace,
        remotes=remotes,
        repositories=repositories,
        profiles=profiles,
        raw_doc=doc,
    )

    selected = profile_name or workspace.default_profile
    manifest.profile(selected)  # raises if unknown

    override = load_override(override_path)
    return manifest, selected, override


def load_override(override_path: Path | None) -> Override:
    """Load a local override document (optional, safe no-op when absent)."""
    if override_path is None or not override_path.is_file():
        return Override(source_path=None)
    doc = load_yaml(override_path)
    version = doc.get("schema_version")
    if version != OVERRIDE_SCHEMA_VERSION:
        raise ManifestError(f"override {override_path}: unexpected schema_version '{version}'")
    repos_raw = doc.get("repositories", {})
    if not isinstance(repos_raw, dict):
        raise ManifestError(f"override {override_path}: 'repositories' must be a mapping")
    repositories = {str(k): dict(v) for k, v in repos_raw.items()}
    return Override(source_path=override_path, repositories=repositories)


def default_override_path(workspace_root: Path) -> Path:
    """Local override location that is always git-ignored."""
    return workspace_root / "overrides" / "local.yaml"
