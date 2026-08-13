"""FuseSoC aggregation: generate fusesoc.conf, core-roots, VLNV index, dep graph.

These files land under `.aix/generated/` (git-ignored).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aixworkflow.models import Manifest, Repository


def _core_roots(manifest: Manifest, repos: list[Repository], workspace_root: Path) -> list[str]:
    """Absolute core-root paths for the enabled repositories."""
    roots: list[str] = []
    for repo in repos:
        for root in repo.fusesoc_roots:
            path = workspace_root / repo.path / root
            roots.append(str(path))
    return roots


def generate_fusesoc_conf(
    manifest: Manifest, repos: list[Repository], workspace_root: Path
) -> str:
    roots = _core_roots(manifest, repos, workspace_root)
    build_root = workspace_root / "build" / "fusesoc"
    cache_root = workspace_root / "cache" / "fusesoc"
    lines = [
        "[main]",
        f"build_root = {build_root}",
        f"cache_root = {cache_root}",
        f"cores_root = {' '.join(roots) if roots else ''}",
        "",
    ]
    return "\n".join(lines)


def generate_core_roots_txt(
    manifest: Manifest, repos: list[Repository], workspace_root: Path
) -> str:
    roots = _core_roots(manifest, repos, workspace_root)
    return "\n".join(roots) + ("\n" if roots else "")


def generate_vlnv_index(
    manifest: Manifest, repos: list[Repository], workspace_root: Path
) -> dict[str, Any]:
    """Scan `*.core` files under each repo's fusesoc roots for VLNV discovery.

    This is a best-effort index; authoritative dependency analysis is done by
    FuseSoC itself at run time.
    """
    index: dict[str, list[dict[str, str]]] = {}
    for repo in repos:
        for root in repo.fusesoc_roots:
            base = workspace_root / repo.path / root
            if not base.is_dir():
                continue
            for core_file in sorted(base.rglob("*.core")):
                if not core_file.is_file():
                    continue
                name = core_file.stem
                index.setdefault(str(core_file), []).append(
                    {"repo": repo.id, "name": name, "path": str(core_file)}
                )
    return index


def generate_dependency_graph_json(
    manifest: Manifest, repos: list[Repository]
) -> dict[str, Any]:
    nodes: list[dict[str, str]] = [
        {
            "id": r.id,
            "type": r.type,
            "path": r.path,
        }
        for r in repos
    ]
    edges = [
        {"from": r.id, "to": dep, "kind": "depends_on"}
        for r in repos
        for dep in r.depends_on
    ]
    return {"nodes": nodes, "edges": edges}


def write_generated_configs(
    manifest: Manifest,
    repos: list[Repository],
    workspace_root: Path,
    *,
    generated_dir: Path | None = None,
) -> Path:
    """Write all generated FuseSoC configs; returns the generated dir."""
    if generated_dir is None:
        generated_dir = workspace_root / manifest.workspace.generated_root
    generated_dir.mkdir(parents=True, exist_ok=True)

    (generated_dir / "fusesoc.conf").write_text(
        generate_fusesoc_conf(manifest, repos, workspace_root), encoding="utf-8"
    )
    (generated_dir / "core-roots.txt").write_text(
        generate_core_roots_txt(manifest, repos, workspace_root), encoding="utf-8"
    )
    (generated_dir / "vlnv-index.json").write_text(
        json.dumps(generate_vlnv_index(manifest, repos, workspace_root), indent=2),
        encoding="utf-8",
    )
    (generated_dir / "dependency-graph.json").write_text(
        json.dumps(generate_dependency_graph_json(manifest, repos), indent=2),
        encoding="utf-8",
    )
    return generated_dir
