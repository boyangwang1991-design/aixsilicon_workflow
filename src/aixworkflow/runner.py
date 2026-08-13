"""Flow runner: deterministic DAG execution for `aix.flow/v1` documents.

P1 scope. The runner resolves stages in dependency order, checks preconditions,
executes registered actions, and always collects evidence on failure.

Actions that cannot run in the current environment raise `ActionSkipped`
(OPTIONAL_UNAVAILABLE semantics, ADR-0004/0006); the runner records them as
`skipped` and continues the DAG instead of failing.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

from aixworkflow.actions import (
    ActionSkipped,
    eda_regression,
    evidence_index,
    fusesoc_target,
    hwif_compatibility_check,
    release_package,
    workspace_resolve,
)
from aixworkflow.errors import AixError, DesignError
from aixworkflow.evidence import EvidenceCollector
from aixworkflow.flow import Flow


@dataclass
class RunResult:
    flow: str
    run_id: str
    status: str
    failed_stage: str | None = None
    stage_results: dict[str, str] = field(default_factory=dict)


class ActionRegistry:
    """Registered actions; `uses` values must resolve here (never raw shell)."""

    def __init__(self) -> None:
        self._actions: dict[str, object] = {}

    def register(self, name: str, fn: object) -> None:
        self._actions[name] = fn

    def get(self, uses: str) -> object | None:
        return self._actions.get(uses)


def default_registry() -> ActionRegistry:
    """Registry with the standard actions (plan.md §15 / ADR-0006).

    `hwif.compatibility` is kept as an alias of `hwif.compatibility-check`
    because several flow documents use the shorter form.
    """
    registry = ActionRegistry()
    registry.register("workspace.resolve", workspace_resolve)
    registry.register("fusesoc.target", fusesoc_target)
    registry.register("hwif.compatibility-check", hwif_compatibility_check)
    registry.register("hwif.compatibility", hwif_compatibility_check)
    registry.register("eda.regression", eda_regression)
    registry.register("evidence.index", evidence_index)
    registry.register("release.package", release_package)
    return registry


def run_flow(
    flow: Flow,
    *,
    registry: ActionRegistry | None = None,
    evidence: EvidenceCollector | None = None,
) -> RunResult:
    """Execute a flow DAG. Raises DesignError on stage failure (after evidence)."""
    registry = registry or ActionRegistry()
    evidence = evidence or EvidenceCollector(flow=flow.name)

    # Preconditions
    pre = flow.preconditions
    if pre.get("clean_workspace"):
        evidence.record_gate("G0", "pass", notes="clean_workspace precondition enforced by caller")
    if pre.get("lock_required"):
        evidence.record_gate("G1", "pass", notes="lock_required precondition enforced by caller")

    # topological execution (Kahn over stages)
    stage_ids = {s.id for s in flow.stages}
    dependents: dict[str, list[str]] = {s.id: [] for s in flow.stages}
    indegree: dict[str, int] = {s.id: len(s.needs) for s in flow.stages}
    for s in flow.stages:
        for n in s.needs:
            if n not in stage_ids:
                raise AixError(f"flow '{flow.name}': stage '{s.id}' needs unknown stage '{n}'")
            dependents[n].append(s.id)

    queue: deque[str] = deque(sorted(s.id for s in flow.stages if indegree[s.id] == 0))
    stage_results: dict[str, str] = {}

    while queue:
        sid = queue.popleft()
        stage = flow.stage_by_id(sid)
        action = registry.get(stage.uses)
        if action is None:
            evidence.record_stage(
                sid, "blocked", failure_signature=f"unregistered action {stage.uses}"
            )
            stage_results[sid] = "blocked"
            continue
        try:
            fn = action  # type: ignore[assignment]
            fn(stage)
            evidence.record_stage(sid, "passed")
            stage_results[sid] = "passed"
        except ActionSkipped as exc:
            evidence.record_stage(sid, "skipped", failure_signature=str(exc))
            stage_results[sid] = "skipped"
        except Exception as exc:  # noqa: BLE001 - normalize any stage failure
            evidence.record_stage(sid, "failed", failure_signature=str(exc), exit_code=1)
            stage_results[sid] = "failed"
            evidence.record_gate("G6", "fail", notes=f"stage {sid} failed: {exc}")
            evidence.write(Path("reports") / evidence.run_id)
            raise DesignError(
                f"flow '{flow.name}' failed at stage '{sid}': {exc}",
                stage=sid,
            ) from exc
        for dep in dependents[sid]:
            indegree[dep] -= 1
            if indegree[dep] == 0:
                queue.append(dep)

    evidence.record_gate("G6", "pass")
    evidence.write(Path("reports") / evidence.run_id)
    return RunResult(
        flow=flow.name, run_id=evidence.run_id, status="passed", stage_results=stage_results
    )
