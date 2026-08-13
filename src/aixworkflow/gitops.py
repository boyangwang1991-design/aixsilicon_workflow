"""Safe git operations.

Security rules (see policies/security-policy.yaml):
- Every command uses `git -C <resolved_repo_path>`; never rely on CWD.
- Arguments are passed as a list, never as shell strings.
- High-risk operations (clean -ffdx, rm -rf, reset --hard, force-push,
  branch delete) require explicit user confirmation.
"""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from aixworkflow.errors import InfraError, SafetyError


@dataclass(frozen=True)
class RepoStatus:
    """Snapshot of a repository's git state."""

    present: bool
    branch: str
    head: str
    dirty: bool
    staged: int
    unstaged: int
    untracked: int
    ahead: int
    behind: int
    upstream: str | None
    remote_url: str | None
    detached: bool


def _run(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    timeout: int = 300,
) -> subprocess.CompletedProcess[str]:
    """Run git with `-C cwd`, returning the CompletedProcess."""
    cmd = ["git"]
    if cwd is not None:
        cmd += ["-C", str(cwd)]
    cmd += list(args)
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise InfraError("git executable not found on PATH") from exc
    except subprocess.TimeoutExpired as exc:
        raise InfraError(f"git command timed out: {' '.join(cmd)}") from exc
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise InfraError(f"git {' '.join(args)} failed ({proc.returncode}): {detail}")
    return proc


def git_available() -> bool:
    return shutil.which("git") is not None


def is_repo(path: Path) -> bool:
    return (path / ".git").exists() or (path / ".git").is_file()


def clone(
    url: str,
    dest: Path,
    *,
    branch: str | None = None,
    shallow: bool = False,
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    args: list[str] = ["clone"]
    if shallow:
        args.append("--depth")
        args.append("1")
    if branch:
        args += ["--branch", branch]
    args += [url, str(dest)]
    _run(args)


def fetch(path: Path, *, all_remotes: bool = False) -> None:
    if all_remotes:
        _run(["fetch", "--all", "--prune"], cwd=path)
    else:
        _run(["fetch", "--prune"], cwd=path)


def current_branch(path: Path) -> tuple[str, bool]:
    """Return (branch_name_or_HEAD_sha, detached)."""
    proc = _run(["symbolic-ref", "--short", "-q", "HEAD"], cwd=path, check=False)
    name = proc.stdout.strip()
    if name:
        return name, False
    head = _run(["rev-parse", "--short", "HEAD"], cwd=path, check=False)
    return (head.stdout.strip() or "?"), True


def head_sha(path: Path) -> str:
    proc = _run(["rev-parse", "HEAD"], cwd=path, check=False)
    if proc.returncode != 0:
        raise InfraError(f"{path}: not a git repository or no HEAD")
    return proc.stdout.strip()


def rev_parse(path: Path, revision: str) -> str | None:
    """Resolve `revision` to a commit SHA, or None when not resolvable."""
    proc = _run(["rev-parse", "--verify", f"{revision}^{{commit}}"], cwd=path, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def rev_parse_any(path: Path, revision: str) -> str | None:
    """Resolve an arbitrary git object expression (e.g. `sha^{tree}`) to a SHA."""
    proc = _run(["rev-parse", "--verify", revision], cwd=path, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def ls_remote(url: str, ref: str) -> str | None:
    """Resolve a ref on a remote URL to a SHA (or None)."""
    proc = _run(["ls-remote", url, ref], check=False)
    if proc.returncode != 0:
        return None
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) == 2 and parts[1] == ref:
            return parts[0].strip()
    return None


def remote_has_branches(url: str) -> bool:
    """Return True when the remote has at least one branch (not an empty repo)."""
    proc = _run(["ls-remote", "--heads", url], check=False)
    if proc.returncode != 0:
        return False
    return bool(proc.stdout.strip())


def remote_url(path: Path, remote: str = "origin") -> str | None:
    proc = _run(["remote", "get-url", remote], cwd=path, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def verify_remote(path: Path, expected_url: str, remote: str = "origin") -> bool:
    actual = remote_url(path, remote)
    return actual is not None and _canonical(actual) == _canonical(expected_url)


def _canonical(url: str) -> str:
    """Normalize SSH/HTTPS forms for comparison."""
    s = url.strip()
    if s.endswith(".git"):
        s = s[:-4]
    for scheme in ("https://", "http://", "ssh://"):
        if s.startswith(scheme):
            return s.split("@", 1)[-1].removeprefix(scheme).replace("/", ":")
    return s


def dirty_status(path: Path) -> tuple[bool, int, int, int]:
    """Return (is_dirty, staged, unstaged, untracked)."""
    proc = _run(["status", "--porcelain=v1"], cwd=path, check=False)
    if proc.returncode != 0:
        return False, 0, 0, 0
    staged = unstaged = untracked = 0
    for line in proc.stdout.splitlines():
        if not line:
            continue
        xy = line[:2]
        if xy == "??":
            untracked += 1
        else:
            if xy[0] != " " and xy[0] != "?":
                staged += 1
            if len(xy) > 1 and xy[1] not in " ?":
                unstaged += 1
    return (staged + unstaged + untracked) > 0, staged, unstaged, untracked


def upstream_relation(path: Path) -> tuple[int, int, str | None]:
    """Return (ahead, behind, upstream_ref)."""
    proc = _run(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=path, check=False)
    if proc.returncode != 0:
        return 0, 0, None
    upstream = proc.stdout.strip()
    proc2 = _run(["rev-list", "--left-right", "--count", "HEAD...@{u}"], cwd=path, check=False)
    if proc2.returncode != 0:
        return 0, 0, upstream
    try:
        ahead_s, behind_s = proc2.stdout.split()
        return int(ahead_s), int(behind_s), upstream
    except ValueError:
        return 0, 0, upstream


def get_status(path: Path, expected_url: str | None = None) -> RepoStatus:
    if not is_repo(path):
        return RepoStatus(
            present=False, branch="", head="", dirty=False, staged=0,
            unstaged=0, untracked=0, ahead=0, behind=0,
            upstream=None, remote_url=None, detached=False,
        )
    branch, detached = current_branch(path)
    head = head_sha(path)
    dirty, staged, unstaged, untracked = dirty_status(path)
    ahead, behind, upstream = upstream_relation(path)
    url = remote_url(path)
    if expected_url is not None:
        actual = url
        url = actual
    return RepoStatus(
        present=True,
        branch=branch,
        head=head[:12],
        dirty=dirty,
        staged=staged,
        unstaged=unstaged,
        untracked=untracked,
        ahead=ahead,
        behind=behind,
        upstream=upstream,
        remote_url=url,
        detached=detached,
    )


def checkout(path: Path, revision: str) -> None:
    _run(["checkout", revision], cwd=path)


def create_branch(path: Path, name: str) -> None:
    _run(["checkout", "-b", name], cwd=path)


def commit(path: Path, message: str) -> None:
    if not message:
        raise SafetyError("commit requires a non-empty message")
    _run(["commit", "-m", message], cwd=path)


def push(path: Path, remote: str = "origin", branch: str | None = None) -> None:
    """Push the current branch to a remote; force-push is never used implicitly."""
    branch = branch or current_branch(path)[0]
    _run(["push", remote, branch], cwd=path)
