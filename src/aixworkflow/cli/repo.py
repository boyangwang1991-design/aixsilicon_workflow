"""`aix repo` command handlers (safe single-repository git wrappers)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from aixworkflow import gitops
from aixworkflow.cli.context import load_context
from aixworkflow.cli.registry import command
from aixworkflow.errors import InfraError


def _repo_path(args: argparse.Namespace) -> tuple[Path, str]:
    ctx = load_context(args)
    repo = ctx.manifest.repo_by_id(args.repo_id)
    return ctx.root / repo.path, repo.id


@command("repo", "status")
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


@command("repo", "diff")
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


@command("repo", "shell")
def _cmd_repo_shell(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    shell = shutil.which("bash") or shutil.which("sh")
    print(f"entering {repo_id} at {path} (ctrl-d to exit)")
    subprocess.run([shell, "-i"], cwd=str(path), check=False)


@command("repo", "branch")
def _cmd_repo_branch(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    gitops.create_branch(path, args.name)
    print(f"{repo_id}: created and checked out branch '{args.name}'")


@command("repo", "commit")
def _cmd_repo_commit(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    gitops.commit(path, args.message)
    print(f"{repo_id}: committed")


@command("repo", "push")
def _cmd_repo_push(args: argparse.Namespace) -> None:
    path, repo_id = _repo_path(args)
    if not gitops.is_repo(path):
        raise InfraError(f"{repo_id}: not cloned at {path}")
    branch = gitops.current_branch(path)[0]
    print(f"{repo_id}: pushing branch '{branch}' to remote '{args.remote}'")
    gitops.push(path, args.remote, branch)
    print(f"{repo_id}: pushed")
