"""Tests for P1 governance/runner additions: exit codes, standard actions,
ActionSkipped semantics, release guard and bundle create."""

from __future__ import annotations

from pathlib import Path

from aixworkflow.errors import (
    EXIT_BLOCKED,
    EXIT_DESIGN_FAILURE,
    EXIT_INFRA_FAILURE,
    EXIT_INPUT_ERROR,
    EXIT_OK,
    BlockedError,
    DesignError,
    InfraError,
    ManifestError,
)
from aixworkflow.flow import Flow, FlowStage
from aixworkflow.runner import ActionRegistry, default_registry, run_flow

# ---------------- exit code contract ----------------


def test_exit_code_contract_values() -> None:
    assert EXIT_OK == 0
    assert EXIT_INPUT_ERROR == 10
    assert EXIT_DESIGN_FAILURE == 20
    assert EXIT_INFRA_FAILURE == 30
    assert EXIT_BLOCKED == 40


def test_error_class_mapping() -> None:
    assert ManifestError("x").exit_code == 10
    assert DesignError("x").exit_code == 20
    assert InfraError("x").exit_code == 30
    assert BlockedError("x").exit_code == 40


# ---------------- standard action registry ----------------


def test_default_registry_registers_standard_actions() -> None:
    reg = default_registry()
    expected = {
        "workspace.resolve",
        "fusesoc.target",
        "hwif.compatibility-check",
        "eda.regression",
        "evidence.index",
        "release.package",
    }
    for name in expected:
        assert reg.get(name) is not None


def test_plugin_tool_absent_reports_unavailable(tmp_path, monkeypatch) -> None:
    # No aixsilicon_tool_repo plugin installed -> `tool` plugin is None.
    from aixworkflow.cli import registry

    monkeypatch.setattr("importlib.metadata.entry_points", lambda group=None: [])
    registry._PLUGINS.clear()
    registry.discover_plugins()
    assert registry.get_plugin("tool") is None


# ---------------- runner ActionSkipped semantics ----------------


def _flow(stages: list[FlowStage]) -> Flow:
    return Flow(
        name="test-flow",
        description="",
        inputs=[],
        preconditions={},
        stages=stages,
        on_failure="fail",
        source_path=Path("test-flow.yaml"),
    )


def test_runner_skips_unavailable_action_and_continues(tmp_path, monkeypatch) -> None:
    from aixworkflow.actions import fusesoc_target

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("shutil.which", lambda _name: None)

    reg = ActionRegistry()
    reg.register("fusesoc.target", fusesoc_target)
    reg.register("evidence.index", lambda stage: None)

    flow = _flow(
        [
            FlowStage("s1", "fusesoc.target", [], {"target": "lint"}, [], None, 0),
            FlowStage("s2", "evidence.index", ["s1"], {}, [], None, 0),
        ]
    )
    result = run_flow(flow, registry=reg)
    assert result.status == "passed"
    assert result.stage_results["s1"] == "skipped"  # OPTIONAL_UNAVAILABLE, not a failure
    assert result.stage_results["s2"] == "passed"


# ---------------- release guard (G7) ----------------


def _ready_workspace(tmp_path, write_manifest, make_git_repo):
    make_git_repo("hwif_repo", {"README.md": "# hwif\n"})
    make_git_repo("vip_repo", {"README.md": "# vip\n"})
    manifest_path = write_manifest()
    from aixworkflow.workspace import init_workspace, sync_workspace

    manifest, profile, override = init_workspace(tmp_path, manifest_path, None)
    sync_workspace(tmp_path, manifest, profile, override)
    return manifest, profile, override


def test_release_guard_allows_clean(tmp_path, write_manifest, make_git_repo) -> None:
    from aixworkflow.workspace import release_guard_ok

    manifest, _profile, override = _ready_workspace(tmp_path, write_manifest, make_git_repo)
    guard = release_guard_ok(manifest, tmp_path, override, require_clean=True)
    assert guard.ok


def test_release_guard_blocks_dirty(tmp_path, write_manifest, make_git_repo) -> None:
    from aixworkflow.workspace import release_guard_ok

    manifest, _profile, override = _ready_workspace(tmp_path, write_manifest, make_git_repo)
    (tmp_path / "repos" / "aixsilicon_hwif_repo" / "scratch.txt").write_text("x", encoding="utf-8")
    guard = release_guard_ok(manifest, tmp_path, override, require_clean=True)
    assert not guard.ok
    assert "dirty" in guard.reason


def test_release_guard_blocks_override(tmp_path, write_manifest, make_git_repo) -> None:
    from aixworkflow.manifest import default_override_path, load_manifest
    from aixworkflow.workspace import release_guard_ok

    _ready_workspace(tmp_path, write_manifest, make_git_repo)
    override_path = default_override_path(tmp_path)
    override_path.parent.mkdir(parents=True, exist_ok=True)
    override_path.write_text(
        "schema_version: aix.workspace-override/v1\n"
        "repositories:\n"
        "  hwif:\n"
        "    revision:\n"
        "      branch: feature/x\n",
        encoding="utf-8",
    )
    manifest, _profile, override = load_manifest(
        tmp_path / "manifests" / "default.yaml", override_path=override_path
    )
    guard = release_guard_ok(manifest, tmp_path, override, require_clean=True)
    assert not guard.ok
    assert "override" in guard.reason


# ---------------- impact gate map from policy ----------------


def test_impact_gate_map_loaded_from_policy() -> None:
    from aixworkflow.impact import _gate_map

    gates = _gate_map()
    assert gates.get("ip") == "ip-smoke"
    assert gates.get("vip") == "axi-vip-unit"
    assert gates.get("soc-integration") == "soc-connect-check"


# ---------------- bundle create + validate ----------------


def test_bundle_create_writes_valid_bundle(tmp_path, monkeypatch) -> None:
    from aixworkflow.cli.extras import _cmd_bundle_create
    from aixworkflow.yamlutil import load_yaml

    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "change-bundle.yaml").write_text(
        "schema_version: aix.change-bundle/v1\n"
        "id: CHG-2026-0001\n"
        "title: example\n"
        "owner: test\n"
        "status: draft\n"
        "repositories: {}\n"
        "validation: {}\n"
        "release_plan: {}\n",
        encoding="utf-8",
    )
    (tmp_path / "changesets").mkdir()
    monkeypatch.chdir(tmp_path)

    args = type("A", (), {"bundle_id": "CHG-2026-0042", "title": "my change", "owner": "test"})()
    _cmd_bundle_create(args)

    doc = load_yaml(tmp_path / "changesets" / "CHG-2026-0042.yaml")
    assert doc["id"] == "CHG-2026-0042"
    assert doc["title"] == "my change"
    assert doc["owner"] == "test"
