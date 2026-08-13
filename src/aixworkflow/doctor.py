"""Environment and workspace diagnostics (`aix wf doctor`)."""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from aixworkflow import gitops
from aixworkflow.graph import DependencyGraph
from aixworkflow.models import Manifest


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


def _check(name: str, ok: bool, detail: str = "") -> Check:
    return Check(name=name, ok=ok, detail=detail)


def run_doctor(manifest: Manifest, workspace_root: Path, profile_name: str) -> list[Check]:
    checks: list[Check] = []

    checks.append(_check("python", True, f"{sys.version_info.major}.{sys.version_info.minor}"))
    checks.append(_check("git", gitops.git_available(), shutil.which("git") or "not found"))
    checks.append(_check("fusesoc", shutil.which("fusesoc") is not None, "optional"))

    repos_root = workspace_root / manifest.workspace.repos_root
    checks.append(_check("repos_root", repos_root.is_dir(), str(repos_root)))

    try:
        graph = DependencyGraph(manifest.repositories)
        graph.ensure_acyclic()
        checks.append(_check("dependency_dag", True, f"{len(manifest.repositories)} repos, acyclic"))
    except Exception as exc:  # pragma: no cover - defensive
        checks.append(_check("dependency_dag", False, str(exc)))

    profile = manifest.profile(profile_name)
    enabled = manifest.enabled_repositories(profile)
    for repo in enabled:
        path = workspace_root / repo.path
        if not gitops.is_repo(path):
            checks.append(_check(f"repo:{repo.id}", False, "not cloned"))
            continue
        ok_remote = gitops.verify_remote(path, repo.remote_url(manifest.remotes))
        checks.append(
            _check(
                f"repo:{repo.id}",
                ok_remote,
                f"remote={'ok' if ok_remote else 'MISMATCH'}; {gitops.head_sha(path)[:12]}",
            )
        )
    return checks
