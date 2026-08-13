"""Revision resolution and lockfile generation."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from pathlib import Path

from aixworkflow import gitops
from aixworkflow.errors import BlockedError, InfraError, ManifestError
from aixworkflow.manifest import Override
from aixworkflow.models import Manifest, Repository

RELEASE_MODE = "release"
WORKSPACE_MODE = "workspace"


@dataclass
class ResolvedRepository:
    id: str
    url: str
    resolved_from: str
    commit: str
    tree: str
    dirty: bool
    overridden: bool

    def to_lock_entry(self) -> dict[str, object]:
        return {
            "url": self.url,
            "resolved_from": self.resolved_from,
            "commit": self.commit,
            "tree": self.tree,
            "dirty": self.dirty,
            "overridden": self.overridden,
        }


@dataclass
class ResolutionResult:
    mode: str
    profile: str
    repositories: list[ResolvedRepository] = field(default_factory=list)
    toolchain: dict[str, object] = field(default_factory=dict)

    def to_lock_doc(self, manifest: Manifest, toolchain: dict[str, object]) -> dict[str, object]:
        repo_doc = {r.id: r.to_lock_entry() for r in self.repositories}
        return {
            "schema_version": "aix.workspace-lock/v1",
            "workspace": manifest.workspace.name,
            "profile": self.profile,
            "manifest_digest": manifest.digest(),
            "resolution_policy": self.mode,
            "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "generator_type": "cli",
            "repositories": repo_doc,
            "toolchain": toolchain,
        }


def _resolve_local(repo: Repository, revision: dict[str, str], path: Path) -> tuple[str, str]:
    """Resolve revision to a full SHA using local refs (after fetch)."""
    if "commit" in revision:
        sha = gitops.rev_parse(path, revision["commit"])
        if sha is None:
            raise InfraError(
                f"repository '{repo.id}': commit {revision['commit']} is not reachable",
                repo=repo.id,
            )
        return sha, revision["commit"]

    if "tag" in revision:
        sha = gitops.rev_parse(path, revision["tag"])
        if sha is None:
            raise InfraError(
                f"repository '{repo.id}': tag {revision['tag']} not found", repo=repo.id
            )
        return sha, f"tag:{revision['tag']}"

    if "branch" in revision:
        branch = revision["branch"]
        candidates = [branch, f"origin/{branch}", f"refs/remotes/origin/{branch}"]
        for cand in candidates:
            sha = gitops.rev_parse(path, cand)
            if sha is not None:
                return sha, f"branch:{branch}"
        raise InfraError(
            f"repository '{repo.id}': branch '{branch}' not resolvable locally", repo=repo.id
        )

    if "range" in revision:
        raise ManifestError(
            f"repository '{repo.id}': 'range' requires explicit resolution and is "
            "not supported for locking"
        )

    raise ManifestError(f"repository '{repo.id}': no revision specified")


def _apply_override(repo: Repository, override: Override) -> tuple[dict[str, str], bool]:
    rev_override = override.revision_for(repo.id)
    return repo.resolved_revision(rev_override), rev_override is not None


def resolve_repository(
    manifest: Manifest,
    repo: Repository,
    override: Override,
    *,
    path: Path,
    mode: str,
    fetch_first: bool = True,
) -> ResolvedRepository:
    """Resolve a single repository's actual commit for the lockfile."""
    revision, overridden = _apply_override(repo, override)
    url = repo.remote_url(manifest.remotes)

    if mode == RELEASE_MODE and overridden:
        raise BlockedError(
            f"repository '{repo.id}' is overridden in release mode; "
            "Release Gate rejects local override",
            repo=repo.id,
        )

    if not gitops.is_repo(path):
        raise InfraError(f"repository '{repo.id}' is not cloned at {path}; run sync first", repo=repo.id)

    if not gitops.verify_remote(path, url):
        raise InfraError(
            f"repository '{repo.id}': configured remote does not match manifest "
            f"(expected {url})",
            repo=repo.id,
        )

    if fetch_first:
        gitops.fetch(path)

    commit, resolved_from = _resolve_local(repo, revision, path)

    tree = gitops.rev_parse(path, f"{commit}^{{tree}}") or ""
    dirty, _, _, _ = gitops.dirty_status(path)

    if mode == RELEASE_MODE and dirty:
        raise BlockedError(
            f"repository '{repo.id}' is dirty in release mode", repo=repo.id
        )

    return ResolvedRepository(
        id=repo.id,
        url=url,
        resolved_from=resolved_from,
        commit=commit,
        tree=tree,
        dirty=dirty,
        overridden=overridden,
    )


def generate_lock(
    manifest: Manifest,
    profile_name: str,
    override: Override,
    *,
    workspace_root: Path,
    mode: str,
    toolchain: dict[str, object] | None = None,
) -> ResolutionResult:
    """Resolve all enabled repositories and produce a lock result."""
    profile = manifest.profile(profile_name)
    repos = manifest.enabled_repositories(profile)
    result = ResolutionResult(mode=mode, profile=profile_name)

    for repo in repos:
        path = workspace_root / repo.path
        result.repositories.append(
            resolve_repository(
                manifest,
                repo,
                override,
                path=path,
                mode=mode,
            )
        )
    if toolchain is None:
        toolchain = {"profile": "unset", "python": "unknown"}
    result.toolchain = dict(toolchain)
    return result


def write_lock(result: ResolutionResult, manifest: Manifest, output: Path) -> None:
    doc = result.to_lock_doc(manifest, result.toolchain)
    from aixworkflow.yamlutil import write_yaml

    write_yaml(output, doc)
