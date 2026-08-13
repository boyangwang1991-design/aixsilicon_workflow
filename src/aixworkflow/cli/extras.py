"""`aix bundle` / `aix release` / `aix tool` handlers (P1/P2)."""

from __future__ import annotations

import argparse
import datetime
from pathlib import Path

from aixworkflow.bundle import load_bundle, validate_merge_order
from aixworkflow.cli.registry import command
from aixworkflow.errors import BlockedError, InfraError, ManifestError
from aixworkflow.yamlutil import load_yaml, write_yaml


def _bundle_path(bundle_id: str) -> Path:
    name = bundle_id if bundle_id.endswith(".yaml") else f"{bundle_id}.yaml"
    candidates = [Path("changesets") / name, Path("changesets") / "examples" / name]
    for path in candidates:
        if path.is_file():
            return path
    raise ManifestError(f"bundle not found under changesets/: {name}")


@command("bundle", "create")
def _cmd_bundle_create(args: argparse.Namespace) -> None:
    """Create a bundle from templates/change-bundle.yaml and validate it."""
    from aixworkflow.schema import validate

    template = Path("templates") / "change-bundle.yaml"
    if not template.is_file():
        raise InfraError(f"template not found: {template}")
    now = datetime.datetime.now(datetime.UTC)
    bundle_id = args.bundle_id or f"CHG-{now:%Y}-0001"
    dest = Path("changesets") / f"{bundle_id}.yaml"
    if dest.is_file():
        raise InfraError(f"bundle already exists (refusing to overwrite): {dest}")

    doc = load_yaml(template)
    doc["id"] = bundle_id
    if getattr(args, "title", None):
        doc["title"] = args.title
    if getattr(args, "owner", None):
        doc["owner"] = args.owner
    # validate in-memory first: never leave an invalid bundle file behind
    validate(doc, "change-bundle", source=str(dest))
    write_yaml(dest, doc)

    bundle = load_bundle(dest)
    order = validate_merge_order(bundle)
    print(f"created bundle {bundle_id}: {dest}")
    print("  merge order:", " -> ".join(order))
    print("  next: edit repositories/branches, then `aix bundle validate`")


@command("bundle", "validate")
def _cmd_bundle_validate(args: argparse.Namespace) -> None:
    path = _bundle_path(args.bundle_id)
    bundle = load_bundle(path)
    order = validate_merge_order(bundle)
    print(f"bundle {bundle.id} [{bundle.status}]: valid")
    print("  merge order:", " -> ".join(order))
    if bundle.repositories:
        print(f"  repositories: {', '.join(r.id for r in bundle.repositories)}")


@command("bundle", "status")
def _cmd_bundle_status(args: argparse.Namespace) -> None:
    path = _bundle_path(args.bundle_id)
    bundle = load_bundle(path)
    print(f"bundle {bundle.id}: status={bundle.status} owner={bundle.owner}")
    for repo in bundle.repositories:
        pr = f"#{repo.pr}" if repo.pr else "-"
        print(
            f"  {repo.id:<16} branch={repo.branch:<28} base={repo.base:<10} pr={pr:<6} order={repo.merge_order}"
        )


@command("tool", "run")
def _cmd_tool_run(args: argparse.Namespace) -> None:
    """Forward `aix tool ...` to the `aix.commands` plugin (ADR-0004).

    Without the `aixsilicon_tool_repo` plugin installed this raises an
    `OPTIONAL_UNAVAILABLE`-style infra error instead of silently no-oping.
    """
    from aixworkflow.cli.registry import get_plugin

    plugin = get_plugin("tool")
    if plugin is None:
        raise InfraError(
            "tool domain unavailable: install aixsilicon_tool_repo (registers the 'tool' "
            "aixsilicon.commands plugin) or use repo-local scripts (OPTIONAL_UNAVAILABLE)"
        )
    plugin(args.args)


def _material_dir(asset: str, version: str) -> Path:
    """Location where release material is staged (runtime, never committed)."""
    root = Path(".aix") / "release" / asset / version
    root.mkdir(parents=True, exist_ok=True)
    return root


@command("release", "prepare")
def _cmd_release_prepare(args: argparse.Namespace) -> None:
    """Collect clean/locked state, qualification evidence and material for a release.

    Gate: refuses to prepare from a dirty tree or active local override
    (plan.md §23 / §24 G7). This is the P2 release coordination entry.
    """
    from aixworkflow.cli.context import load_context
    from aixworkflow.evidence import EvidenceCollector
    from aixworkflow.release import build_release_material

    ctx = load_context(args)
    material = build_release_material(
        asset=args.asset,
        version=args.version,
        manifest=ctx.manifest,
        profile=ctx.profile,
        override=ctx.override,
        root=ctx.root,
    )
    out = _material_dir(args.asset, args.version)
    manifest_path = out / "release_manifest.yaml"
    manifest_path.write_text(material["manifest_yaml"], encoding="utf-8")
    evidence = EvidenceCollector(flow=f"release:{args.asset}:{args.version}")
    evidence.record_gate(
        "G7", "pass", notes="release material prepared (approval still required to publish)"
    )
    evidence.write(out / "evidence")
    print(f"release material staged: {out}")
    print(f"  asset   : {args.asset}")
    print(f"  version : {args.version}")
    print(
        "  gate    : G0-G6 clean/locked confirmed; G7 human approval required before `aix release publish`"
    )
    print(f"  manifest: {manifest_path}")


@command("release", "publish")
def _cmd_release_publish(args: argparse.Namespace) -> None:
    """Idempotently record and report a published release (no duplicate).

    Does NOT perform git tag/push/GitHub release automatically (plan.md §3.2);
    it records the approval-gated publication and requires clean/locked state.
    """
    from aixworkflow.cli.context import load_context
    from aixworkflow.release import already_published, load_release_state, mark_published
    from aixworkflow.workspace import release_guard_ok

    ctx = load_context(args)
    guard = release_guard_ok(ctx.manifest, ctx.root, ctx.override, require_clean=True)
    if not guard.ok:
        raise BlockedError(f"release publish blocked: {guard.reason}")

    state_path = Path(".aix") / "release-state.json"
    state = load_release_state(state_path)
    if already_published(state, args.asset, args.version):
        print(f"release already published: {args.asset} {args.version} (idempotent, nothing to do)")
        return
    mark_published(state_path, args.asset, args.version, run_id="approval-gated")
    print(f"published: {args.asset} {args.version}")
    print("  recorded in .aix/release-state.json (idempotent)")
    print(
        "  NOTE: git tag/push + GitHub Release + Catalog PR are NOT auto-performed (plan.md §3.2)"
    )
