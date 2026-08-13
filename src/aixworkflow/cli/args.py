"""Argument parser construction for all `aix` command domains."""

from __future__ import annotations

import argparse

from aixworkflow import __version__
from aixworkflow.resolver import RELEASE_MODE, WORKSPACE_MODE


def build_parser() -> argparse.ArgumentParser:
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
    p_sync.add_argument("--lock", default=None, help="lockfile to sync against (release semantics)")
    p_sync.add_argument("--manifest", default=None, help="manifest path")

    p_status = wf_sub.add_parser("status", help="show workspace status table")
    p_status.add_argument("--dirty", action="store_true", help="only show dirty repositories")
    p_status.add_argument("--profile", default=None)
    p_status.add_argument("--manifest", default=None)

    wf_sub.add_parser("doctor", help="environment and workspace diagnostics")

    p_lock = wf_sub.add_parser("lock", help="generate a resolved lockfile")
    p_lock.add_argument("-o", "--output", default=None, help="output path (default .aix/local.lock.yaml)")
    p_lock.add_argument("--mode", choices=[WORKSPACE_MODE, RELEASE_MODE], default=WORKSPACE_MODE)
    p_lock.add_argument("--no-fetch", action="store_true", help="resolve from local refs only (offline)")
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

    p_run = wf_sub.add_parser("run", help="execute a standard flow (DAG runner)")
    p_run.add_argument("flow", help="flow name under workflows/ (e.g. ip-verification)")
    p_run.add_argument("--profile", default=None)
    p_run.add_argument("--manifest", default=None)

    p_test = wf_sub.add_parser("test", help="impact-driven verification (affected analysis)")
    p_test.add_argument("--affected", action="store_true", help="analyze impact of a changed repo")
    p_test.add_argument("--repo", required=True, help="repository id whose change is being evaluated")
    p_test.add_argument("--paths", default=None, help="comma separated changed file paths")
    p_test.add_argument("--profile", default=None)
    p_test.add_argument("--manifest", default=None)

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

    # ---- bundle / release ----
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

    return parser
