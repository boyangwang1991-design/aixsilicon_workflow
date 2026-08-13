"""`aix wf` command handlers."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from aixworkflow import gitops
from aixworkflow.cli.context import load_context, workspace_root
from aixworkflow.cli.registry import command
from aixworkflow.doctor import run_doctor
from aixworkflow.errors import AixError, InfraError, SafetyError
from aixworkflow.evidence import EvidenceCollector
from aixworkflow.flow import load_flow
from aixworkflow.graph import DependencyGraph
from aixworkflow.resolver import RELEASE_MODE, WORKSPACE_MODE, write_lock
from aixworkflow.runner import default_registry, run_flow
from aixworkflow.workspace import (
    diff_against_lock,
    ensure_runtime_dirs,
    generate_lock_for_profile,
    init_workspace,
    sync_workspace,
    workspace_status,
    write_fusesoc_configs,
)
from aixworkflow.yamlutil import load_yaml


@command("wf", "init")
def _cmd_wf_init(args: argparse.Namespace) -> None:
    root = workspace_root()
    manifest_path = Path(getattr(args, "manifest", None) or "manifests/default.yaml")
    manifest, selected, override = init_workspace(
        root, manifest_path, getattr(args, "profile", None)
    )
    ensure_runtime_dirs(root, manifest)
    print(f"workspace initialized: profile={selected}, manifest={manifest_path}")
    if override.source_path is not None:
        print("NOTE: local override present -> NON-BASELINE")
    print("next: run `aix wf sync`")


@command("wf", "sync")
def _cmd_wf_sync(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    locked: dict[str, str] | None = None
    if args.lock:
        lock_doc = load_yaml(Path(args.lock))
        repos_doc = lock_doc.get("repositories", {})
        locked = {str(k): str(v.get("commit", "")) for k, v in repos_doc.items() if v.get("commit")}
    mode = RELEASE_MODE if args.lock else WORKSPACE_MODE
    report = sync_workspace(
        ctx.root,
        ctx.manifest,
        ctx.profile,
        ctx.override,
        repo_filter=args.repo,
        mode=mode,
        locked=locked,
    )
    print(f"profile={ctx.profile}")
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


@command("wf", "status")
def _cmd_wf_status(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    rows = workspace_status(ctx.root, ctx.manifest, ctx.profile, ctx.override)
    print(f"profile={ctx.profile}  manifest={ctx.manifest.source_path}")
    print(
        f"{'REPO':<16} {'BRANCH':<22} {'HEAD':<13} {'BASELINE':<10} {'DIRTY':<6} {'REMOTE':<8} {'OVR':<5} {'EN':<4}"
    )
    for repo, status, enabled, overridden in rows:
        if args.dirty and not status.dirty:
            continue
        if not status.present:
            state = "MISSING" if repo.required else "OPT-UNAVAIL"
            print(f"{repo.id:<16} {state}")
            continue
        if status.ahead and status.behind:
            baseline = "diverged"
        elif status.ahead:
            baseline = "ahead"
        elif status.behind:
            baseline = "behind"
        else:
            baseline = "clean"
        dirty = "YES" if status.dirty else "no"
        remote = "sync" if (status.ahead == 0 and status.behind == 0) else "dirty"
        overridden_s = "YES" if overridden else "-"
        enabled_s = "yes" if enabled else "-"
        print(
            f"{repo.id:<16} {status.branch:<22} {status.head:<13} {baseline:<10} {dirty:<6} {remote:<8} {overridden_s:<5} {enabled_s:<4}"
        )
    if ctx.override.source_path is not None:
        print("NON-BASELINE / OVERRIDDEN: overrides/local.yaml is active")


@command("wf", "doctor")
def _cmd_wf_doctor(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    checks = run_doctor(ctx.manifest, ctx.root, ctx.profile)
    failed = 0
    for check in checks:
        flag = "OK " if check.ok else "FAIL"
        if not check.ok:
            failed += 1
        print(f"[{flag}] {check.name}: {check.detail}")
    print("doctor complete")
    if failed:
        raise InfraError(f"doctor found {failed} problem(s)")


@command("wf", "lock")
def _cmd_wf_lock(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    result = generate_lock_for_profile(
        ctx.root,
        ctx.manifest,
        ctx.profile,
        ctx.override,
        mode=args.mode,
        fetch_first=not args.no_fetch,
    )
    output = Path(args.output) if args.output else ctx.root / ".aix" / "local.lock.yaml"
    write_lock(result, ctx.manifest, output)
    mode_note = " (offline, no fetch)" if args.no_fetch else ""
    print(
        f"lock written: {output} ({args.mode} mode{mode_note}, {len(result.repositories)} repositories)"
    )


@command("wf", "diff")
def _cmd_wf_diff(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    result = diff_against_lock(Path(args.against), ctx.manifest, ctx.root)
    diffs = result["diff"]
    if isinstance(diffs, list) and diffs:
        print("differences vs lock:")
        for d in diffs:
            print(f"  {d['repo']:<16} locked={d['locked']} current={d['current']}")
    else:
        print("no differences vs lock")


@command("wf", "graph")
def _cmd_wf_graph(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    profile = ctx.manifest.profile(ctx.profile)
    repos = ctx.manifest.enabled_repositories(profile)
    graph = DependencyGraph(repos)
    print(f"profile={ctx.profile}  enabled={len(repos)}")
    print("topological order:", " -> ".join(graph.topological_order()))
    cycles = graph.find_cycles()
    if cycles:
        print("CYCLES DETECTED:", cycles)
        raise InfraError("dependency DAG contains cycle(s)")


@command("wf", "fusesoc")
def _cmd_wf_fusesoc(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    gen_dir = write_fusesoc_configs(ctx.root, ctx.manifest, ctx.profile)
    print(f"generated FuseSoC configs under {gen_dir}")


@command("wf", "clean")
def _cmd_wf_clean(args: argparse.Namespace) -> None:
    """Remove generated build dirs only; never touches repos/ or reports/."""
    root = workspace_root()
    from aixworkflow.safety import allowed_clean_dirs

    for rel in allowed_clean_dirs():
        target = root / rel
        if target.is_dir():
            shutil.rmtree(target)
            print(f"removed {target}")
    print("clean complete (repos/ and reports/ untouched)")


@command("wf", "run")
def _cmd_wf_run(args: argparse.Namespace) -> None:
    """Execute a standard flow DAG with the standard action set (plan.md §15)."""
    flow_path = Path("workflows") / f"{args.flow}.yaml"
    if not flow_path.is_file():
        raise InfraError(f"flow not found: {flow_path}")
    flow = load_flow(flow_path)

    registry = default_registry()
    evidence = EvidenceCollector(flow=flow.name)
    result = run_flow(flow, registry=registry, evidence=evidence)

    for sid, status in result.stage_results.items():
        print(f"  stage {sid:<22} {status}")
    skipped = [s for s, st in result.stage_results.items() if st == "skipped"]
    blocked = [s for s, st in result.stage_results.items() if st == "blocked"]
    print(f"run_id={result.run_id}  status={result.status}")
    if skipped:
        print(f"note: {len(skipped)} stage(s) skipped (OPTIONAL_UNAVAILABLE): {skipped}")
    if blocked:
        print(
            f"note: {len(blocked)} stage(s) blocked (provider unavailable / not yet "
            f"implemented): {blocked}\n"
            f"      blocked != failed; evidence recorded. Gate enforcement is separate (G0-G7)."
        )
    print(f"evidence under reports/{evidence.run_id}")


@command("wf", "test")
def _cmd_wf_test(args: argparse.Namespace) -> None:
    """Impact-driven verification: compute the affected set and required gates."""
    if not args.affected:
        raise AixError("aix wf test currently requires --affected")
    ctx = load_context(args)
    from aixworkflow.graph import DependencyGraph
    from aixworkflow.impact import analyze_impact

    graph = DependencyGraph(ctx.manifest.repositories)
    paths = [p for p in (args.paths or "").split(",") if p]
    result = analyze_impact(
        ctx.manifest,
        graph,
        repo_id=args.repo,
        changed_paths=paths or None,
    )
    print(f"change repository: {result.repository}  paths: {result.paths}")
    print(f"direct affected : {result.direct or '-'}")
    print(f"transitive      : {result.transitive or '-'}")
    print("required gates  :")
    for gate in result.required_gates:
        print(f"  - {gate}")
    if result.recommended_gates:
        print("recommended     :")
        for gate in result.recommended_gates:
            print(f"  - {gate}")
    if result.unknown_dependencies:
        print(f"UNKNOWN deps (expand coverage): {result.unknown_dependencies}")


@command("wf", "foreach")
def _cmd_wf_foreach(args: argparse.Namespace) -> None:
    ctx = load_context(args)
    if not args.cmd:
        raise SafetyError("foreach requires a command")
    # foreach defaults to read-only; mutating commands require --allow-write (future).
    profile = ctx.manifest.profile(ctx.profile)
    repos = ctx.manifest.enabled_repositories(profile)
    for repo in repos:
        path = ctx.root / repo.path
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
