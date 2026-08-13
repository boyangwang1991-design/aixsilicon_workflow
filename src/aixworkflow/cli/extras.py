"""`aix bundle` / `aix release` handlers (P1/P2)."""

from __future__ import annotations

import argparse
from pathlib import Path

from aixworkflow.bundle import load_bundle, validate_merge_order
from aixworkflow.cli.registry import command
from aixworkflow.errors import ManifestError


def _bundle_path(bundle_id: str) -> Path:
    name = bundle_id if bundle_id.endswith(".yaml") else f"{bundle_id}.yaml"
    candidates = [Path("changesets") / name, Path("changesets") / "examples" / name]
    for path in candidates:
        if path.is_file():
            return path
    raise ManifestError(f"bundle not found under changesets/: {name}")


@command("bundle", "create")
def _cmd_bundle_create(args: argparse.Namespace) -> None:
    print("bundle create: copy templates/change-bundle.yaml into changesets/ then `aix bundle validate`")


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
        print(f"  {repo.id:<16} branch={repo.branch:<28} base={repo.base:<10} pr={pr:<6} order={repo.merge_order}")


@command("release", "prepare")
def _cmd_release_prepare(args: argparse.Namespace) -> None:
    print(
        f"release prepare --asset {args.asset} --version {args.version}: "
        "collects clean/locked state, qualification gates and material (P2)"
    )
