"""Unit tests: safety guards, flow loading/validation, bundle, evidence."""

from __future__ import annotations

from pathlib import Path

import pytest

from aixworkflow.bundle import ChangeBundle, load_bundle, validate_merge_order
from aixworkflow.errors import DesignError, ManifestError
from aixworkflow.evidence import EvidenceCollector
from aixworkflow.flow import assert_registered_action, load_flow
from aixworkflow.runner import ActionRegistry, run_flow
from aixworkflow.safety import is_high_risk
from aixworkflow.yamlutil import dump_yaml

# ---------------- safety ----------------


def test_high_risk_detection():
    assert is_high_risk("git clean -ffdx")
    assert is_high_risk("rm -rf repos/*")
    assert is_high_risk("git push --force origin main")
    assert not is_high_risk("git status")


def test_guard_requires_confirmation(tmp_path):
    from aixworkflow.safety import guard_high_risk

    result = guard_high_risk("git reset --hard", workspace_root=tmp_path, confirmed=False)
    assert not result.allowed
    ok = guard_high_risk("git reset --hard", workspace_root=tmp_path, confirmed=True)
    assert ok.allowed


# ---------------- flow ----------------

_FLOW_DOC = {
    "schema_version": "aix.flow/v1",
    "name": "smoke",
    "description": "test flow",
    "inputs": ["ip_vlnv"],
    "preconditions": {"lock_required": True},
    "stages": [
        {"id": "resolve", "uses": "workspace.resolve"},
        {"id": "lint", "needs": ["resolve"], "uses": "fusesoc.target", "with": {"target": "lint"}},
        {"id": "unit", "needs": ["lint"], "uses": "eda.regression"},
        {"id": "evidence", "needs": ["resolve", "lint", "unit"], "uses": "evidence.index"},
    ],
}


def test_load_flow(tmp_path):
    path = tmp_path / "flow.yaml"
    path.write_text(dump_yaml(_FLOW_DOC), encoding="utf-8")
    flow = load_flow(path)
    assert flow.name == "smoke"
    assert len(flow.stages) == 4


def test_flow_rejects_bad_schema(tmp_path):
    doc = dict(_FLOW_DOC)
    doc["schema_version"] = "bad"
    path = tmp_path / "bad.yaml"
    path.write_text(dump_yaml(doc), encoding="utf-8")
    with pytest.raises(ManifestError):
        load_flow(path)


def test_assert_registered_action():
    assert_registered_action("fusesoc.target")
    with pytest.raises(ManifestError):
        assert_registered_action("evil; rm -rf /")


def test_run_flow_success(tmp_path):
    path = tmp_path / "flow.yaml"
    path.write_text(dump_yaml(_FLOW_DOC), encoding="utf-8")
    flow = load_flow(path)
    registry = ActionRegistry()
    registry.register("workspace.resolve", lambda s: None)
    registry.register("fusesoc.target", lambda s: None)
    registry.register("eda.regression", lambda s: None)
    registry.register("evidence.index", lambda s: None)
    # flow declares lock_required; provide the lock so G1 passes (F-002).
    result = run_flow(flow, registry=registry, lock_present=True)
    assert result.status == "passed"


def test_run_flow_failure_collects_evidence(tmp_path):
    path = tmp_path / "flow.yaml"
    path.write_text(dump_yaml(_FLOW_DOC), encoding="utf-8")
    flow = load_flow(path)
    registry = ActionRegistry()
    registry.register("workspace.resolve", lambda s: None)
    registry.register(
        "fusesoc.target", lambda s: (_ for _ in ()).throw(RuntimeError("lint failed"))
    )
    with pytest.raises(DesignError) as excinfo:
        run_flow(flow, registry=registry, lock_present=True)
    assert "lint" in str(excinfo.value)


def test_run_flow_blocked_when_lock_missing(tmp_path):
    """F-002: lock_required with no lock must block the flow, not pass."""
    from aixworkflow.runner import BlockedPrecondition

    path = tmp_path / "flow.yaml"
    path.write_text(dump_yaml(_FLOW_DOC), encoding="utf-8")
    flow = load_flow(path)
    registry = ActionRegistry()
    registry.register("workspace.resolve", lambda s: None)
    with pytest.raises(BlockedPrecondition) as excinfo:
        run_flow(flow, registry=registry)
    assert excinfo.value.gate == "G1"


# ---------------- bundle ----------------

_BUNDLE_DOC = {
    "schema_version": "aix.change-bundle/v1",
    "id": "CHG-2026-0042",
    "title": "AXI USER sideband",
    "owner": "wang-boyang",
    "status": "validating",
    "repositories": {
        "hwif": {"branch": "feature/a", "base": "main", "pr": 1, "merge_order": 1},
        "vip": {
            "branch": "feature/b",
            "base": "main",
            "pr": 2,
            "depends_on": ["hwif"],
            "merge_order": 2,
        },
        "ip": {
            "branch": "feature/c",
            "base": "main",
            "pr": 3,
            "depends_on": ["hwif", "vip"],
            "merge_order": 3,
        },
    },
    "validation": {"profile": "ip-dev", "flow": "cross-repo-qualification"},
    "release_plan": {"hwif": "2.0.0", "vip": "1.4.0", "ip": "1.1.0"},
}


def test_load_bundle_and_merge_order(tmp_path):
    path = tmp_path / "bundle.yaml"
    path.write_text(dump_yaml(_BUNDLE_DOC), encoding="utf-8")
    bundle = load_bundle(path)
    assert isinstance(bundle, ChangeBundle)
    order = validate_merge_order(bundle)
    assert order.index("hwif") < order.index("vip") < order.index("ip")


def test_bundle_merge_cycle(tmp_path):
    doc = {
        "schema_version": "aix.change-bundle/v1",
        "id": "CHG-2026-0001",
        "title": "cycle",
        "owner": "x",
        "status": "draft",
        "repositories": {
            "a": {"branch": "fa", "base": "main", "depends_on": ["b"]},
            "b": {"branch": "fb", "base": "main", "depends_on": ["a"]},
        },
    }
    path = tmp_path / "cycle.yaml"
    path.write_text(dump_yaml(doc), encoding="utf-8")
    bundle = load_bundle(path)
    with pytest.raises(ManifestError):
        validate_merge_order(bundle)


# ---------------- evidence ----------------


def test_evidence_collector_writes(tmp_path):
    collector = EvidenceCollector(flow="ip-verification")
    collector.record_stage("lint", "passed")
    collector.record_gate("G4", "pass")
    artifact = tmp_path / "report.log"
    artifact.write_text("ok", encoding="utf-8")
    collector.add_artifact(artifact)
    out = collector.write(tmp_path / "reports" / collector.run_id)
    assert (out / "run_manifest.yaml").is_file()
    assert (out / "evidence_index.yaml").is_file()
    assert (out / "status.json").is_file()


def test_schema_parity(tmp_path):
    """Package-embedded schemas must match the repo-level schemas (drift guard)."""
    import json

    # Explicit UTF-8 keeps parity checks locale-independent on Windows (F-013).
    repo_schemas = sorted((Path("schemas").resolve()).glob("*.json"))
    assert repo_schemas, "repo schemas directory missing"
    pkg_dir = Path("src/aixworkflow/schemas")
    for repo_schema in repo_schemas:
        pkg_schema = pkg_dir / repo_schema.name
        assert pkg_schema.is_file(), f"missing packaged schema {pkg_schema}"
        assert json.loads(repo_schema.read_text(encoding="utf-8")) == json.loads(
            pkg_schema.read_text(encoding="utf-8")
        ), f"schema drift: {repo_schema.name}"
