"""Standard flow actions for the aix runner (plan.md §15, ADR-0004 / ADR-0006).

Actions are deterministic and structured: they call the `aix tool` plugin when
available, and fall back to repo-local scripts during the migration window
(ADR-0006 phase A). They never execute arbitrary shell strings from flow YAML
(policies/security-policy.yaml): `eda.regression` accepts an explicit argv list
only.

Actions that cannot run in the current environment raise `ActionSkipped`; the
runner records them as `skipped` (with reason) and continues the DAG instead of
failing — mirroring the `OPTIONAL_UNAVAILABLE` semantics of optional skills.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from aixworkflow.flow import FlowStage
from aixworkflow.graph import DependencyGraph


class ActionSkipped(Exception):
    """Raised when an action cannot run in the current environment.

    The runner records the stage as `skipped` (with reason) and continues;
    it is never treated as a design failure.
    """


def _find_repo_script(repo_dir: str, rel: str) -> Path:
    candidate = Path("repos") / repo_dir / rel
    if candidate.is_file():
        return candidate
    raise ActionSkipped(f"repo script not found: {candidate} (migrates to aix tool per ADR-0006)")


def _run_cmd(cmd: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()[-500:]
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{detail}")


def _load_manifest_ctx(stage: FlowStage):
    from aixworkflow.manifest import default_override_path, load_manifest

    manifest_path = Path("manifests") / str(stage.with_.get("manifest", "default.yaml"))
    profile_name = stage.with_.get("profile")
    manifest, profile, override = load_manifest(
        manifest_path, profile_name=profile_name, override_path=default_override_path(Path("."))
    )
    return manifest, profile, override


def workspace_resolve(stage: FlowStage) -> None:
    """Validate the manifest DAG and generate FuseSoC aggregation configs."""
    manifest, profile, _override = _load_manifest_ctx(stage)
    DependencyGraph(manifest.repositories).ensure_acyclic()
    from aixworkflow.workspace import write_fusesoc_configs

    write_fusesoc_configs(Path("."), manifest, profile)


def fusesoc_target(stage: FlowStage) -> None:
    """Run FuseSoC for the requested target when fusesoc is installed."""
    target = str(stage.with_.get("target", "lint"))
    vlnv = stage.with_.get("vlnv")
    tool = stage.with_.get("tool")
    if shutil.which("fusesoc") is None:
        raise ActionSkipped(
            "fusesoc CLI not installed; configs were validated by workspace.resolve"
        )
    if vlnv:
        cmd = ["fusesoc", "--cores-root", "repos", "run", "--target", target]
        if tool:
            cmd += ["--tool", str(tool)]
        cmd.append(str(vlnv))
        _run_cmd(cmd)
    else:
        # discovery/compile smoke across all cores roots
        _run_cmd(["fusesoc", "--cores-root", "repos", "core", "list"])


def hwif_compatibility_check(stage: FlowStage) -> None:
    """Interface compatibility judgement (DIRECT/ADAPTER_REQUIRED/INCOMPATIBLE).

    Phase A fallback calls the hwif repo-local checker; migrates to
    `aix tool hwif compatibility` once tool_repo is available (ADR-0006).
    Missing input files are treated as skipped, never a hard failure.
    """
    producer = stage.with_.get("producer")
    consumer = stage.with_.get("consumer")
    if not producer or not consumer:
        raise ActionSkipped(
            "hwif.compatibility-check requires `producer` and `consumer` in stage.with"
        )
    producer_path = Path(str(producer))
    consumer_path = Path(str(consumer))
    if not producer_path.is_file() or not consumer_path.is_file():
        raise ActionSkipped(
            "hwif.compatibility-check inputs not present in workspace "
            f"(producer/consumer files: {producer_path}, {consumer_path})"
        )
    script = _find_repo_script(
        "aixsilicon_hwif_repo", "tools/compatibility_check/compatibility_check.py"
    )
    _run_cmd([sys.executable, str(script), str(producer), str(consumer)])


def eda_regression(stage: FlowStage) -> None:
    """Run a registered EDA/regression command (explicit argv list only)."""
    cmd = stage.with_.get("command")
    if not isinstance(cmd, list) or not cmd:
        raise ActionSkipped(
            "eda.regression requires `command: [argv...]` in stage.with (never a shell string)"
        )
    _run_cmd([str(c) for c in cmd])


def release_package(stage: FlowStage) -> None:
    """Stage release material for an asset (G7 guard enforced inside)."""
    asset = stage.with_.get("asset")
    version = stage.with_.get("version")
    if not asset or not version:
        raise ActionSkipped("release.package requires `asset` and `version` in stage.with")
    manifest, profile, override = _load_manifest_ctx(stage)
    from aixworkflow.release import build_release_material

    build_release_material(
        asset=str(asset),
        version=str(version),
        manifest=manifest,
        profile=profile,
        override=override,
        root=Path("."),
    )


def evidence_index(stage: FlowStage) -> None:
    """Evidence collection is owned by the runner; this action is a schema sanity marker."""
    from aixworkflow import schema  # noqa: F401

    if not stage:
        return
