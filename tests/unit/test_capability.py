"""WF-004 / TOOL-001: action capability registry + preflight (ADR-0008).

Covers:
- 6-state evaluation (available / optional-unavailable / unimplemented /
  version-mismatch / environment-unavailable)
- required vs optional (skill.*) blocking
- preflight capability matrix + blocked stages
- registry contract metadata
"""

from __future__ import annotations

from aixworkflow.capability import (
    AVAILABLE,
    ENVIRONMENT_UNAVAILABLE,
    OPTIONAL_UNAVAILABLE,
    UNIMPLEMENTED,
    CapabilityRegistry,
    default_registry,
)
from aixworkflow.flow import Flow, FlowStage


def _flow(stages: list[FlowStage]) -> Flow:
    return Flow(
        name="cap-test",
        description="",
        inputs=[],
        preconditions={},
        stages=stages,
        on_failure="collect_evidence_then_fail",
        source_path=__import__("pathlib").Path("cap-test.yaml"),
    )


def _stage(sid: str, uses: str) -> FlowStage:
    return FlowStage(sid, uses, [], {}, [], None, 0)


def test_six_states_values():
    assert AVAILABLE == "available"
    assert OPTIONAL_UNAVAILABLE == "optional-unavailable"
    assert UNIMPLEMENTED == "unimplemented"
    assert ENVIRONMENT_UNAVAILABLE == "environment-unavailable"


def test_available_required_stage_passes_preflight():
    reg = CapabilityRegistry()
    reg.register("workspace.resolve", provider="builtin", available=True)
    result = reg.preflight(_flow([_stage("s1", "workspace.resolve")]))
    assert result.ok
    assert result.entries[0].state == AVAILABLE
    assert result.blocked == []


def test_unimplemented_required_stage_blocks():
    reg = CapabilityRegistry()
    # action not registered -> unimplemented for required
    result = reg.preflight(_flow([_stage("s1", "tool.schema")]))
    assert not result.ok
    assert result.entries[0].state == UNIMPLEMENTED
    assert result.blocked == ["s1"]


def test_optional_unavailable_does_not_block():
    reg = CapabilityRegistry()
    # skill.* is always optional
    result = reg.preflight(_flow([_stage("s1", "skill.ip.spec")]))
    assert result.ok
    assert result.entries[0].state == OPTIONAL_UNAVAILABLE
    assert result.blocked == []


def test_registered_but_not_available_is_unimplemented():
    reg = CapabilityRegistry()
    reg.register("fusesoc.target", provider="fusesoc", environment=("fusesoc",))
    result = reg.preflight(_flow([_stage("s1", "fusesoc.target")]))
    assert not result.ok
    assert result.entries[0].state == UNIMPLEMENTED
    assert result.blocked == ["s1"]


def test_environment_unavailable_detection(tmp_path, monkeypatch):
    reg = CapabilityRegistry()
    reg.register(
        "fusesoc.target",
        provider="fusesoc",
        environment=("fusesoc",),
        available=True,
    )
    monkeypatch.setattr("shutil.which", lambda _name: None)
    result = reg.preflight(_flow([_stage("s1", "fusesoc.target")]))
    assert not result.ok
    assert result.entries[0].state == ENVIRONMENT_UNAVAILABLE
    assert result.blocked == ["s1"]


def test_preflight_matrix_contains_all_stages():
    reg = CapabilityRegistry()
    reg.register("workspace.resolve", provider="builtin", available=True)
    flow = _flow([_stage("s1", "workspace.resolve"), _stage("s2", "tool.schema")])
    result = reg.preflight(flow)
    matrix = result.matrix()
    assert {m["stage"] for m in matrix} == {"s1", "s2"}
    states = {m["state"] for m in matrix}
    assert AVAILABLE in states
    assert UNIMPLEMENTED in states


def test_default_registry_has_known_contracts():
    reg = default_registry()
    contracts = reg.contracts()
    assert "workspace.resolve" in contracts
    assert "evidence.index" in contracts
    # action inventory gap remains for tool.* / catalog.* / soc.* (F-004)
    assert "tool.schema" not in contracts
