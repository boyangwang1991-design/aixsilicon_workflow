"""High-level workspace operations: init, sync, status, lock, diff, graph.

These orchestrate the low-level modules while enforcing the safety policies
from policies/security-policy.yaml.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aixworkflow import gitops
from aixworkflow.errors import BlockedError, InfraError, ManifestError
from aixworkflow.fusesoc import write_generated_configs
from aixworkflow.graph import DependencyGraph
from aixworkflow.manifest import (
    Override,
    default_override_path,
    load_manifest,
)
from aixworkflow.models import Manifest, Repository
from aixworkflow.resolver import (
    RELEASE_MODE,
    WORKSPACE_MODE,
    ResolutionResult,
    generate_lock,
)
from aixworkflow.state import WorkspaceState, python_version


@dataclass
class SyncReport:
    cloned: list[str]
    fetched: list[str]
    checked_out: list[str]
    skipped: list[str]
    optional_unavailable: list[str]


def ensure_runtime_dirs(workspace_root: Path, manifest: Manifest) -> None:
    """Create runtime directories (repos, .aix/generated, build, cache, reports)."""
    dirs = [
        workspace_root / manifest.workspace.repos_root,
        workspace_root / manifest.workspace.generated_root,
        workspace_root / "build",
        workspace_root / "cache",
        workspace_root / "reports",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def init_workspace(
    workspace_root: Path,
    manifest_path: Path,
    profile_name: str | None,
) -> tuple[Manifest, str, Override]:
    """Initialize the workspace and record local state."""
    manifest, selected, override = load_manifest(
        manifest_path, profile_name=profile_name, override_path=default_override_path(workspace_root)
    )
    ensure_runtime_dirs(workspace_root, manifest)

    # Validate the dependency DAG at init time.
    DependencyGraph(manifest.repositories).ensure_acyclic()

    state = WorkspaceState(workspace_root=workspace_root).load()
    state.manifest_path = str(manifest_path)
    state.profile = selected
    state.initialized = True
    state.save()
    return manifest, selected, override


def _load_workspace(workspace_root: Path, profile_name: str | None, manifest_path: Path | None):
    """Load the active manifest/state; used by sync/status/lock."""
    state = WorkspaceState(workspace_root=workspace_root).load()
    path = manifest_path or (Path(state.manifest_path) if state.manifest_path else None)
    if path is None:
        default = workspace_root / "manifests" / "default.yaml"
        if default.is_file():
            path = default
        else:
            raise ManifestError(
                "no manifest found; run `aix wf init --profile <name>` first"
            )
    manifest, selected, override = load_manifest(
        Path(path), profile_name=profile_name, override_path=default_override_path(workspace_root)
    )
    return manifest, selected, override


def sync_workspace(
    workspace_root: Path,
    manifest: Manifest,
    profile_name: str,
    override: Override,
    *,
    repo_filter: str | None = None,
    mode: str = WORKSPACE_MODE,
    locked: dict[str, str] | None = None,
) -> SyncReport:
    """Clone/fetch/checkout all enabled repositories for the profile.

    When `locked` (repo_id -> commit sha, from a lockfile) is given, the mode
    must be RELEASE_MODE and the locked commit is force-checked-out.
    """
    profile = manifest.profile(profile_name)
    enabled = manifest.enabled_repositories(profile)
    if repo_filter:
        enabled = [r for r in enabled if r.id == repo_filter]
        if not enabled:
            raise ManifestError(f"repository '{repo_filter}' is not enabled for profile '{profile_name}'")

    report = SyncReport(cloned=[], fetched=[], checked_out=[], skipped=[], optional_unavailable=[])

    for repo in enabled:
        url = repo.remote_url(manifest.remotes)
        path = workspace_root / repo.path

        if not gitops.is_repo(path):
            try:
                gitops.clone(url, path, branch=repo.revision.get("branch"), shallow=repo.checkout.shallow)
                report.cloned.append(repo.id)
                continue
            except InfraError:
                if not repo.required and repo.visibility == "private":
                    report.optional_unavailable.append(repo.id)
                    print(f"[{repo.id}] OPTIONAL_UNAVAILABLE (private repo not accessible); skipped")
                    continue
                if not gitops.remote_has_branches(url):
                    raise InfraError(
                        f"repository '{repo.id}' exists at {url} but is empty "
                        f"(no branches); create an initial commit on "
                        f"'{repo.revision.get('branch', 'main')}' first",
                        repo=repo.id,
                    ) from None
                raise

        # Existing repo: verify remote before touching anything.
        if not gitops.verify_remote(path, url):
            raise InfraError(
                f"repository '{repo.id}': configured remote does not match manifest "
                f"(expected {url}); refusing to continue",
                repo=repo.id,
            )

        # Release gate: local override is forbidden.
        if mode == RELEASE_MODE and override.revision_for(repo.id) is not None:
            raise BlockedError(
                f"repository '{repo.id}' is overridden in release mode; "
                "Release Gate rejects local override",
                repo=repo.id,
            )

        # Do not auto-checkout/reset when dirty.
        dirty, _, _, _ = gitops.dirty_status(path)
        if dirty:
            if mode == RELEASE_MODE:
                raise BlockedError(
                    f"repository '{repo.id}' is dirty in release mode", repo=repo.id
                )
            report.skipped.append(repo.id)
            continue

        try:
            gitops.fetch(path)
            report.fetched.append(repo.id)
        except InfraError as exc:
            if not repo.required and repo.visibility == "private":
                report.optional_unavailable.append(repo.id)
                print(f"[{repo.id}] OPTIONAL_UNAVAILABLE; fetch failed ({exc}); skipped")
                continue
            raise

        # Locked mode: force-checkout the lockfile commit.
        locked_sha = (locked or {}).get(repo.id)
        if locked_sha is not None:
            if mode != RELEASE_MODE:
                raise BlockedError(
                    f"repository '{repo.id}': --lock requires release mode", repo=repo.id
                )
            resolved = gitops.rev_parse_any(path, locked_sha)
            if resolved is None:
                raise InfraError(
                    f"repository '{repo.id}': locked commit {locked_sha} is not reachable",
                    repo=repo.id,
                )
            current = gitops.head_sha(path)
            if current != resolved:
                gitops.checkout(path, locked_sha)
                report.checked_out.append(repo.id)
            continue

        # Resolve the target revision from override or manifest.
        rev_override = override.revision_for(repo.id)
        revision = repo.resolved_revision(rev_override)

        branch = revision.get("branch")
        tag = revision.get("tag")
        commit = revision.get("commit")

        target = None
        if branch:
            target = branch
        elif tag:
            target = tag
        elif commit:
            target = commit

        if target is not None:
            resolved = gitops.rev_parse(path, target)
            if resolved is None:
                resolved_remote = gitops.rev_parse(path, f"origin/{target}") if branch else None
                if resolved_remote is None:
                    raise InfraError(
                        f"repository '{repo.id}': revision '{target}' is not reachable "
                        f"(branch={branch}, tag={tag}, commit={commit})",
                        repo=repo.id,
                    )
                target = resolved_remote
            current = gitops.head_sha(path)
            if current != resolved:
                gitops.checkout(path, target)
                report.checked_out.append(repo.id)
        else:
            raise ManifestError(f"repository '{repo.id}': no resolvable revision")

    return report


def workspace_status(
    workspace_root: Path,
    manifest: Manifest,
    profile_name: str,
    override: Override,
) -> list[tuple[Repository, gitops.RepoStatus, bool, bool]]:
    """Return (repo, status, enabled, overridden) for every repository."""
    profile = manifest.profile(profile_name)
    enabled_ids = {r.id for r in manifest.enabled_repositories(profile)}
    rows: list[tuple[Repository, gitops.RepoStatus, bool, bool]] = []
    for repo in manifest.repositories:
        path = workspace_root / repo.path
        url = repo.remote_url(manifest.remotes) if gitops.is_repo(path) else None
        status = gitops.get_status(path, url)
        overridden = override.revision_for(repo.id) is not None
        rows.append((repo, status, repo.id in enabled_ids, overridden))
    return rows


def generate_lock_for_profile(
    workspace_root: Path,
    manifest: Manifest,
    profile_name: str,
    override: Override,
    mode: str,
    *,
    fetch_first: bool = True,
) -> ResolutionResult:
    toolchain = {"profile": "unset", "python": python_version()}
    return generate_lock(
        manifest,
        profile_name,
        override,
        workspace_root=workspace_root,
        mode=mode,
        toolchain=toolchain,
        fetch_first=fetch_first,
    )


def write_fusesoc_configs(
    workspace_root: Path,
    manifest: Manifest,
    profile_name: str,
) -> Path:
    profile = manifest.profile(profile_name)
    repos = manifest.enabled_repositories(profile)
    return write_generated_configs(manifest, repos, workspace_root)


def diff_against_lock(lock_path: Path, manifest: Manifest, workspace_root: Path) -> dict[str, object]:
    """Compare the current checkout SHAs against a lockfile."""
    from aixworkflow.yamlutil import load_yaml

    lock = load_yaml(lock_path)
    lock_repos = lock.get("repositories", {})
    result: dict[str, object] = {"diff": [], "missing_repos": []}
    diffs: list[dict[str, str]] = []
    for repo_id, entry in lock_repos.items():
        repo = manifest.repo_by_id(repo_id)
        path = workspace_root / repo.path
        if not gitops.is_repo(path):
            result["missing_repos"]  # type: ignore[union-attr]
            continue
        current = gitops.head_sha(path)
        locked = str(entry.get("commit", ""))
        if current != locked:
            diffs.append(
                {
                    "repo": repo_id,
                    "locked": locked[:12],
                    "current": current[:12],
                }
            )
    result["diff"] = diffs
    return result


def manifest_digest_of(manifest: Manifest) -> str:
    return manifest.digest()
