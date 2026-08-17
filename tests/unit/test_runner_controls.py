"""WF-005: runner fail-closed control semantics.

Covers (F-001/F-002/F-006/F-007):
- unregistered required action blocks the flow (never summarized as pass)
- write_scope escape is refused before execution
- timeout enforcement
- retry semantics
- G0/G1 precondition real judgement (dirty workspace blocks)
- G6 pass only when all stages passed
"""

from __future__ import annotations

from pathlib import Path

import pytest

from aixworkflow.errors import DesignError
from aixworkflow.flow import Flow, FlowStage
from aixworkflow.runner import ActionRegistry, BlockedPrecondition, run_flow


def _flow(stages: list[FlowStage], **pre) -> Flow:
    return Flow(
        name="ctl-test",
        description="",
        inputs=[],
        preconditions=pre,
        stages=stages,
        on_failure="collect_evidence_then_fail",
        source_path=Path("ctl-test.yaml"),
    )


def _stage(sid: str, uses: str, **kw) -> FlowStage:
    return FlowStage(
        id=sid,
        uses=uses,
        needs=list(kw.pop("needs", [])),
        with_=dict(kw.pop("with", {})),
        write_scope=list(kw.pop("write_scope", [])),
        timeout_seconds=kw.pop("timeout_seconds", None),
        retries=int(kw.pop("retries", 0)),
    )


def test_unregistered_required_action_blocks_flow(tmp_path):
    reg = ActionRegistry()
    reg.register("evidence.index", lambda s: None)
    flow = _flow([_stage("s1", "tool.schema"), _stage("s2", "evidence.index", needs=["s1"])])
    result = run_flow(flow, registry=reg)
    assert result.status == "blocked"
    assert result.failed_stage == "s1"
    assert result.stage_results["s1"] == "blocked"


def test_write_scope_escape_refused(tmp_path):
    reg = ActionRegistry()
    reg.register("tool.reg", lambda s: None)
    # write_scope path escapes the workspace root
    stage = _stage(
        "s1",
        "tool.reg",
        write_scope=[{"repo": "ip", "paths": ["../outside"]}],
    )
    flow = _flow([stage])
    with pytest.raises(DesignError):
        run_flow(flow, registry=reg, root=tmp_path)


def test_timeout_enforced(tmp_path):
    import time

    def _slow(_s) -> None:
        time.sleep(2)

    reg = ActionRegistry()
    reg.register("eda.regression", _slow)
    stage = _stage("s1", "eda.regression", timeout_seconds=1)
    flow = _flow([stage])
    with pytest.raises(DesignError):
        run_flow(flow, registry=reg)


def test_retry_retries_then_succeeds(tmp_path):
    calls = {"n": 0}

    def _flaky(_s) -> None:
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("transient failure")

    reg = ActionRegistry()
    reg.register("eda.regression", _flaky)
    stage = _stage("s1", "eda.regression", retries=2)
    flow = _flow([stage])
    result = run_flow(flow, registry=reg)
    assert result.status == "passed"
    assert calls["n"] == 3


def test_dirty_workspace_blocks_g0(tmp_path):
    reg = ActionRegistry()
    reg.register("workspace.resolve", lambda s: None)
    flow = _flow([_stage("s1", "workspace.resolve")], clean_workspace=True)
    with pytest.raises(BlockedPrecondition) as excinfo:
        run_flow(flow, registry=reg, workspace_clean=False)
    assert excinfo.value.gate == "G0"


def test_clean_workspace_passes_g0(tmp_path):
    reg = ActionRegistry()
    reg.register("workspace.resolve", lambda s: None)
    flow = _flow([_stage("s1", "workspace.resolve")], clean_workspace=True)
    result = run_flow(flow, registry=reg, workspace_clean=True)
    assert result.status == "passed"


def test_g6_fails_when_stage_fails(tmp_path):
    reg = ActionRegistry()

    def _boom(_s) -> None:
        raise RuntimeError("boom")

    reg.register("eda.regression", _boom)
    flow = _flow([_stage("s1", "eda.regression")])
    with pytest.raises(DesignError):
        run_flow(flow, registry=reg)


def test_override_active_blocks_g2(tmp_path):
    reg = ActionRegistry()
    reg.register("workspace.resolve", lambda s: None)
    flow = _flow([_stage("s1", "workspace.resolve")], forbid_local_override=True)
    with pytest.raises(BlockedPrecondition) as excinfo:
        run_flow(flow, registry=reg, override_active=True)
    assert excinfo.value.gate == "G2"
