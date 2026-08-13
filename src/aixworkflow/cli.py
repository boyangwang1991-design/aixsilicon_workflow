"""`aix` command-line interface.

Command domains:
- `aix wf`   workspace commands (init/sync/status/doctor/lock/diff/graph/fusesoc)
- `aix repo` single-repository git wrappers (status/shell/branch/commit/push/diff)
- `aix bundle` / `aix release` (stubs for later phases)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from aixworkflow import __version__, gitops
from aixworkflow.doctor import run_doctor
from aixworkflow.errors import AixError, InfraError, SafetyError
from aixworkflow.graph import DependencyGraph
from aixworkflow.manifest import default_override_path, load_manifest
from aixworkflow.resolver import RELEASE_MODE, WORKSPACE_MODE, write_lock
from aixworkflow.workspace import (
    diff_against_lock,
    ensure_runtime_dirs,
    generate_lock_for_profile,
    init_workspace,
    sync_workspace,
    workspace_status,
    write_fusesoc_configs,
)

DEFAULT_MANIFEST = "manifests/default.yaml"


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="aix",
        description="AIXSILICON multi-repo workspace control plane",
    )
    parser.add_argument("--version", action="version", version=f"aix {__version__}")
    sub = parser.add_subparsers(dest="domain", required=True)

    # ---- wf ----
    wf = sub.add_parser("wf", help="workspace commands")
    wf_sub = wf.add_subparsers(dest="command", required=True)

    p_init = wf_sub.add_parser("init", help="initialize the workspace")
    p_init.add_argument("--profile", default=None, help="profile to select (default from manifest)")
    p_init.add_argument("--manifest", default=None, help="manifest path (default manifests/default.yaml)")

    p_sync = wf_sub.add_parser("sync", help="clone/fetch/checkout repositories")
    p_sync.add_argument("--repo", default=None, help="only sync this repository id")
    p_sync.add_argument("--profile", default=None, help="profile to select")
    p_sync.add_argument("--lock", default=None, help="lockfile to sync against (future)")
    p_sync.add_argument("--manifest", default=None, help="manifest path")

    p_status = wf_sub.add_parser("status", help="show workspace status table")
    p_status.add_argument("--dirty", action="store_true", help="only show dirty repositories")
    p_status.add_argument("--profile", default=None)
    p_status.add_argument("--manifest", default=None)

    wf_sub.add_parser("doctor", help="environment and workspace diagnostics")

    p_lock = wf_sub.add_parser("lock", help="generate a resolved lockfile")
    p_lock.add_argument("-o", "--output", default=None, help="output path (default .aix/local.lock.yaml)")
    p_lock.add_argument("--mode", choices=[WORKSPACE_MODE, RELEASE_MODE], default=WORKSPACE_MODE)
    p_lock.add_argument("--profile", default=None)
    p_lock.add_argument("--manifest", default=None)

    p_diff = wf_sub.add_parser("diff", help="diff current SHAs against a lockfile")
    p_diff.add_argument("--against", required=True, help="lockfile path to compare against")
    p_diff.add_argument("--profile", default=None)
    p_diff.add_argument("--manifest", default=None)

    p_graph = wf_sub.add_parser("graph", help="print the repository dependency graph")
    p_graph.add_argument("--profile", default=None)
    p_graph.add_argument("--manifest", default=None)

    p_fuse = wf_sub.add_parser("fusesoc", help="generate FuseSoC aggregation configs")
    p_fuse.add_argument("--generate", action="store_true", help="write generated configs")
    p_fuse.add_argument("--profile", default=None)
    p_fuse.add_argument("--manifest", default=None)

    wf_sub.add_parser("clean", help="safely remove generated build/cache dirs (never repos/)")

    p_foreach = wf_sub.add_parser("foreach", help="run a read-only command in every enabled repo")
    p_foreach.add_argument("--repo", default=None)
    p_foreach.add_argument("--profile", default=None)
    p_foreach.add_argument("--manifest", default=None)
    p_foreach.add_argument("cmd", nargs=argparse.REMAINDER)

    # ---- repo ----
    repo = sub.add_parser("repo", help="single-repository git wrappers")
    repo_sub = repo.add_subparsers(dest="command", required=True)

    p_rstatus = repo_sub.add_parser("status", help="show status of one repository")
    p_rstatus.add_argument("repo_id")
    p_rstatus.add_argument("--manifest", default=None)

    p_rdiff = repo_sub.add_parser("diff", help="show diff of one repository")
    p_rdiff.add_argument("repo_id")
    p_rdiff.add_argument("--manifest", default=None)

    p_rshell = repo_sub.add_parser("shell", help="start a shell in one repository")
    p_rshell.add_argument("repo_id")
    p_rshell.add_argument("--manifest", default=None)

    p_rbranch = repo_sub.add_parser("branch", help="create a feature branch in one repository")
    p_rbranch.add_argument("repo_id")
    p_rbranch.add_argument("name")
    p_rbranch.add_argument("--manifest", default=None)

    p_rcommit = repo_sub.add_parser("commit", help="commit in one repository only")
    p_rcommit.add_argument("repo_id")
    p_rcommit.add_argument("-m", "--message", required=True)
    p_rcommit.add_argument("--manifest", default=None)

    p_rpush = repo_sub.add_parser("push", help="push one repository (no force by default)")
    p_rpush.add_argument("repo_id")
    p_rpush.add_argument("--remote", default="origin")
    p_rpush.add_argument("--manifest", default=None)

    # ---- bundle / release (stubs) ----
    bundle = sub.add_parser("bundle", help="cross-repo change bundles (P1)")
    bundle_sub = bundle.add_subparsers(dest="command", required=True)
    bundle_sub.add_parser("create", help="create a bundle from a template")
    bv = bundle_sub.add_parser("validate", help="validate a bundle")
    bv.add_argument("bundle_id")
    bs = bundle_sub.add_parser("status", help="show bundle status")
    bs.add_argument("bundle_id")

    release = sub.add_parser("release", help="release coordination (P2)")
    release_sub = release.add_subparsers(dest="command", required=True)
    rp = release_sub.add_parser("prepare", help="prepare release material")
    rp.add_argument("--asset", required=True)
    rp.add_argument("--version", required=True)

    return parser.parse_args(argv)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _workspace_root() -> Path:
    return Path.cwd()


def _resolve_manifest(args: argparse.Namespace) -> tuple[Path, str | None]:
    manifest_path = Path(getattr(args, "manifest", None) or DEFAULT_MANIFEST)
    return manifest_path, getattr(args, "profile", None)


def _load_workspace_context(args: argparse.Namespace):
    """Load the active manifest, profile and override for wf/repo commands."""
    root = _workspace_root()
    manifest_path, profile = _resolve_manifest(args)
    manifest, selected, override = load_manifest(
        manifest_path, profile_name=profile, override_path=default_override_path(root)
    )
    return root, manifest, selected, override


def _print_status_row(repo_id: str, *fields: str) -> None:
    print(f"{repo_id:<16} " + "  ".join(f"{f:<10}" for f in fields))


# --------------------------------------------------------------------------
# wf commands
# --------------------------------------------------------------------------

def _cmd_wf_init(args: argparse.Namespace) -> None:
    root = _workspace_root()
    manifest_path, profile = _resolve_manifest(args)
    manifest, selected, override = init_workspace(root, manifest_path, profile)
    ensure_runtime_dirs(root, manifest)
    print(f"workspace initialized: profile={selected}, manifest={manifest_path}")
    if override.source_path is not None:
        print("NOTE: local override present -> NON-BASELINE")
    print("next: run `aix wf sync`")


def _cmd_wf_sync(args: argparse.Namespace) -> None:
    root, manifest, selected, override = _load_workspace_context(args)
    mode = RELEASE_MODE if args.lock else WORKSPACE_MODE
    report = sync_workspace(
        root, manifest, selected, override, repo_filter=args.repo, mode=mode
    )
    print(f"profile={selected}")
    if report.cloned:
        print(f"cloned     : {', '.join(report.cloned)}")
    if report.fetched:
        print(f"fetched    : {', '.join(report.fetched)}")
    if report.checked_out:
        print(f"checked out: {', '.join(report.checked_out)}")
    if report.skipped:
        print(f"skipped    : {', '.join(report.skipped)} (dirty, not touched)")
    if report.optional_unavailable:
        print(f"OPTIONAL_UNAVAILABLE: {', '.join(report.optional_unavailable)}")


def _cmd_wf_status(args: argparse.Namespace) -> None:
    root, manifest, selected, override = _load_workspace_context(args)
    rows = workspace_status(root, manifest, selected, override)
    print(f"profile={selected}  manifest={manifest.source_path}")
    print(f"{'REPO':<16} {'BRANCH':<22} {'HEAD':<13} {'BASELINE':<10} {'DIRTY':<6} {'REMOTE':<8} {'OVR':<5} {'EN':<4}")
    for repo, status, enabled, overridden in rows:
        if args.dirty and not status.dirty:
            continue
        if not status.present:
            state = "MISSING" if repo.required else "OPT-UNAVAIL"
            print(f"{repo.id:<16} {state}")
            continue
        baseline = "ahead" if status.ahead else ("behind" if status.behind else ("diverged" if status.ahead and status.behind else "clean"))
        dirty = "YES" if status.dirty else "no"
        remote = "sync" if (status.ahead == 0 and status.behind == 0) else "dirty"
        overridden_s = "YES" if overridden else "-"
        enabled_s = "yes" if enabled else "-"
        print(
            f"{repo.id:<16} {status.branch:<22} {status.head:<13} {baseline:<10} {dirty:<6} {remote:<8} {overridden_s:<5} {enabled_s:<4}"
        )
    if override.source_path is not None:
        print("NON-BASELINE / OVERRIDDEN: overrides/local.yaml is active")


def _cmd_wf_doctor(args: argparse.Namespace) -> None:
    root, manifest, selected, _ = _load_workspace_context(args)
    checks = run_doctor(manifest, root, selected)
    failed = 0
    for check in checks:
        flag = "OK " if check.ok else "FAIL"
        if not check.ok:
            failed += 1
        print(f"[{flag}] {check.name}: {check.detail}")
    print("doctor complete")
    if failed:
        raise InfraError(f"doctor found {failed} problem(s)")


def _cmd_wf_lock(args: argparse.Namespace) -> None:
    root, manifest, selected, override = _load_workspace_context(args)
    result = generate_lock_for_profile(root, manifest, selected, override, mode=args.mode)
    output = Path(args.output) if args.output else root / ".aix" / "local.lock.yaml"
    write_lock(result, manifest, output)
    print(f"lock written: {output} ({args.mode} mode, {len(result.repositories)} repositories)")


def _cmd_wf_diff(args: argparse.Namespace) -> None:
    root, manifest, selected, _ = _load_workspace_context(args)
    result = diff_against_lock(Path(args.against), manifest, root)
    diffs = result["diff"]
    if isinstance(diffs, list) and diffs:
        print("differences vs lock:")
        for d in diffs:
            print(f"  {d['repo']:<16} locked={d['locked']} current={d['current']}")
    else:
        print("no differences vs lock")


def _cmd_wf_graph(args: argparse.Namespace) -> None:
    root, manifest, selected, _ = _load_workspace_context(args)
    profile = manifest.profile(selected)
    repos = manifest.enabled_repositories(profile)
    graph = DependencyGraph(repos)
    print(f"profile={selected}  enabled={len(repos)}")
    print("topological order:", " -> ".join(graph.topological_order()))
    cycles = graph.find_cycles()
    if cycles:
        print("CYCLES DETECTED:", cycles)
        raise InfraError("dependency DAG contains cycle(s)")


def _cmd_wf_fusesoc(args: argparse.Namespace) -> None:
    root, manifest, selected, _ = _load_workspace_context(args)
    gen_dir = write_fusesoc_configs(root, manifest, selected)
    print(f"generated FuseSoC configs under {gen_dir}")


def _cmd_wf_clean(args: argparse.Namespace) -> None:
    """Remove generated build dirs only; never touches repos/ or reports/."""
    root = _workspace_root()
    import shutil

    from aixworkflow.safety import allowed_clean_dirs

    for rel in allowed_clean_dirs():
        target = root / rel
        if target.is_dir():
            shutil.rmtree(target)
            print(f"removed {target}")
    print("clean complete (repos/ and reports/ untouched)")


def _cmd_wf_foreach(args: argparse.Namespace) -> None:
    root, manifest, selected, _ = _load_workspace_context(args)
    if not args.cmd:
        raise SafetyError("foreach requires a command")
    # foreach defaults to read-only; mutating commands require --allow-write.
    profile = manifest.profile(selected)
    repos = manifest.enabled_repositories(profile)
    for repo in repos:
        path = root / repo.path
        if not gitops.is_repo(path):
            print(f"[{repo.id}] MISSING")
            continue
        print(f"=== {repo.id} ===")
        proc = subprocess.run(
            args.cmd,
            cwd=str(path),
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.stderr:
            print(proc.stderr.rstrip(), file=sys.stderr)


# --------------------------------------------------------------------------
# repo commands
# --------------------------------------------------------------------------

def _repo_path(args: argparse.Namespace) -> tuple[Path, str]:
    root, manifest, selected, override = _load_workspace_context(args)
    repo = manifest.repo_by_id(args.repo_id)
    return root / repo.path, repo.id


def _cmd_repo_status(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    status = gitops.get_status(path)
    if not status.present:
        print(f"{repo_id}: not cloned at {path}")
        return
    print(f"{repo_id}: branch={status.branch} head={status.head} dirty={status.dirty}")
    print(f"  staged={status.staged} unstaged={status.unstaged} untracked={status.untracked}")
    print(f"  ahead={status.ahead} behind={status.behind} upstream={status.upstream}")
    print(f"  remote={status.remote_url}")


def _cmd_repo_diff(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    proc = subprocess.run(
        ["git", "-C", str(path), "diff", "--stat"],
        text=True,
        capture_output=True,
        check=False,
    )
    print(proc.stdout.rstrip() or f"{repo_id}: clean")
    if proc.stderr:
        print(proc.stderr.rstrip(), file=sys.stderr)


def _cmd_repo_shell(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    shell = shutil.which("bash") or shutil.which("sh")
    print(f"entering {repo_id} at {path} (ctrl-d to exit)")
    subprocess.run([shell, "-i"], cwd=str(path), check=False)


def _cmd_repo_branch(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    gitops.create_branch(path, args.name)
    print(f"{repo_id}: created and checked out branch '{args.name}'")


def _cmd_repo_commit(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    gitops.commit(path, args.message)
    print(f"{repo_id}: committed")


def _cmd_repo_push(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    branch = gitops.current_branch(path)[0]
    print(f"{repo_id}: pushing branch '{branch}' to remote '{args.remote}'")
    gitops.push(path, args.remote, branch)
    print(f"{repo_id}: pushed")


# --------------------------------------------------------------------------
# bundle / release stubs
# --------------------------------------------------------------------------

def _cmd_bundle(args: argparse.Namespace) -> None:
    if args.command == "create":
        print("bundle create: use templates/change-bundle.yaml (P1 implementation pending)")
    elif args.command == "validate":
        print(f"bundle validate {args.bundle_id}: P1 implementation pending")
    elif args.command == "status":
        print(f"bundle status {args.bundle_id}: P1 implementation pending")


def _cmd_release(args: argparse.Namespace) -> None:
    if args.command == "prepare":
        print(f"release prepare --asset {args.asset} --version {args.version}: P2 implementation pending")


# --------------------------------------------------------------------------
# dispatch
# --------------------------------------------------------------------------

_HANDLERS: dict[str, Any] = {
    "init": _cmd_wf_init,
    "sync": _cmd_wf_sync,
    "status": _cmd_wf_status,
    "doctor": _cmd_wf_doctor,
    "lock": _cmd_wf_lock,
    "diff": _cmd_wf_diff,
    "graph": _cmd_wf_graph,
    "fusesoc": _cmd_wf_fusesoc,
    "clean": _cmd_wf_clean,
    "foreach": _cmd_wf_foreach,
}

_REPO_HANDLERS: dict[str, Any] = {
    "status": _cmd_repo_status,
    "diff": _cmd_repo_diff,
    "shell": _cmd_repo_shell,
    "branch": _cmd_repo_branch,
    "commit": _cmd_repo_commit,
    "push": _cmd_repo_push,
}


def main(argv: Sequence[str] | None = None) -> None:
    args = _parse_args(argv)
    try:
        if args.domain == "wf":
            _HANDLERS[args.command](args)
        elif args.domain == "repo":
            _REPO_HANDLERS[args.command](args)
        elif args.domain == "bundle":
            _cmd_bundle(args)
        elif args.domain == "release":
            _cmd_release(args)
        else:
            raise AixError(f"unknown domain: {args.domain}")
    except AixError as exc:
        prefix = f"[{exc.category}]"
        location = f" repo={exc.repo}" if exc.repo else ""
        stage = f" stage={exc.stage}" if exc.stage else ""
        print(f"{prefix}{location}{stage}: {exc.message}", file=sys.stderr)
        sys.exit(exc.exit_code)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
