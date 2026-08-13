"""Unified command context: resolve manifest/profile/override once per run."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from aixworkflow.manifest import Override, default_override_path, load_manifest
from aixworkflow.models import Manifest

DEFAULT_MANIFEST = "manifests/default.yaml"


@dataclass
class Context:
    root: Path
    manifest: Manifest
    profile: str
    override: Override


def workspace_root() -> Path:
    return Path.cwd()


def load_context(args: argparse.Namespace) -> Context:
    """Load the active manifest, selected profile and local override once."""
    root = workspace_root()
    manifest_path = Path(getattr(args, "manifest", None) or DEFAULT_MANIFEST)
    manifest, selected, override = load_manifest(
        manifest_path,
        profile_name=getattr(args, "profile", None),
        override_path=default_override_path(root),
    )
    return Context(root=root, manifest=manifest, profile=selected, override=override)
