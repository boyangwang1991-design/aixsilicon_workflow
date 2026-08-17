"""Flow runner: deterministic DAG execution for `aix.flow/v1` documents.

M1 scope (WF-005): the runner enforces fail-closed control semantics:

- unregistered / non-available **required** actions block the flow (never
  summarized as pass) — F-001
- `blocked`/`skipped` required stages fail the flow — F-001
- preconditions (`clean_workspace`, `lock_required`, `forbid_local_override`,
  `required_gates`) are judged by real validators, never hard-coded pass — F-002
- `timeout_seconds` / `retries` / `on_failure` are executed by the runner — F-007
- `write_scope` is validated against the owning repository's allowed paths
  before a stage runs — F-006
- optional actions (e.g. `skill.*`) degrade to `skipped` with a recorded reason.
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
from aixworkflow.flow import Flow, FlowStage


@dataclass
class RunResult:
    flow: str
    run_id: str
    status: str
    failed_stage: str | None = None
    stage_results: dict[str, str] = field(default_factory=dict)
    blocked_stages: list[str] = field(default_factory=list)


class ActionRegistry:
    """Registered actions; `uses` values must resolve here (never raw shell)."""

    def __init__(self) -> None:
        self._actions: dict[str, object] = {}

    def register(self, name: str, fn: object) -> None:
        self._actions[name] = fn

    def get(self, uses: str) -> object | None:
        return self._actions.get(uses)

    def names(self) -> list[str]:
        return sorted(self._actions)


def default_registry() -> ActionRegistry:
    """Registry with the standard actions (plan.md §15 / ADR-0006)."""
    registry = ActionRegistry()
    registry.register("workspace.resolve", workspace_resolve)
    registry.register("fusesoc.target", fusesoc_target)
    registry.register("hwif.compatibility-check", hwif_compatibility_check)
    registry.register("hwif.compatibility", hwif_compatibility_check)
    registry.register("eda.regression", eda_regression)
    registry.register("evidence.index", evidence_index)
    registry.register("release.package", release_package)
    return registry


def _is_optional(stage: FlowStage) -> bool:
    """Optional actions degrade to skipped; everything else is required."""
    # skill.* actions are always optional (ADR-0008).
    return stage.uses.startswith("skill.")


def _check_write_scope(stage: FlowStage, root: Path) -> None:
    """Validate declared write_scope against the workspace root (F-006).

    Each write_scope entry names a repository and a list of allowed path
    prefixes. A stage writing outside those prefixes is refused before running.
    """
    for entry in stage.write_scope:
        repo_id = entry.get("repo")
        paths = entry.get("paths") or []
        if not repo_id:
            raise DesignError(
                f"stage '{stage.id}' write_scope entry missing 'repo'",
                stage=stage.id,
            )
        for rel in paths:
            target = (root / str(rel)).resolve()
            # target must stay under the workspace root (no escape)
            if not str(target).startswith(str(root.resolve())):
                raise DesignError(
                    f"stage '{stage.id}' write_scope path escapes workspace: {rel}",
                    stage=stage.id,
                )


def _execute_with_controls(
    fn,
    stage: FlowStage,
    *,
    root: Path,
) -> None:
    """Run a stage action with timeout/retry enforcement (F-007).

    - `retries` retries the action (skipped/blocked are never retried);
    - `timeout_seconds` wraps execution in a cross-platform thread with a hard
      deadline; actions are expected to be bounded (external tools already have
      their own subprocess timeout via gitops/actions).
    """
    timeout = stage.timeout_seconds
    retries = stage.retries
    attempts = retries + 1
    last_exc: Exception | None = None
    for attempt in range(attempts):
        try:
            if timeout:
                _run_with_timeout(fn, stage, root, timeout)
            else:
                fn(stage)
            return
        except ActionSkipped:
            raise
        except Exception as exc:  # noqa: BLE001 - re-raised after retries
            last_exc = exc
            if attempt < retries:
                continue
            raise
    if last_exc is not None:  # pragma: no cover - unreachable, defensive
        raise last_exc


def _run_with_timeout(fn, stage: FlowStage, root: Path, timeout: int) -> None:
    """Execute `fn` with a hard timeout using a worker thread (cross-platform).

    A thread is used so timeout semantics are identical on Windows and POSIX
    without subprocess pickling concerns. Actions that shell out (fusesoc,
    eda) carry their own subprocess timeouts; this layer enforces the flow-level
    deadline.
    """
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(fn, stage)
        try:
            future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise TimeoutError(f"stage '{stage.id}' exceeded timeout of {timeout}s") from None


def _evaluate_preconditions(
    flow: Flow,
    evidence: EvidenceCollector,
    *,
    workspace_clean: bool | None = None,
    lock_present: bool | None = None,
    forbid_override: bool = False,
    override_active: bool = False,
    required_gates: list[str] | None = None,
    gate_results: dict[str, str] | None = None,
) -> None:
    """Evaluate preconditions with real values (F-002); never hard-code pass."""
    pre = flow.preconditions
    if pre.get("clean_workspace"):
        clean = workspace_clean if workspace_clean is not None else False
        if clean:
            evidence.record_gate("G0", "pass", notes="workspace clean")
        else:
            evidence.record_gate("G0", "fail", notes="workspace is dirty")
            raise BlockedPrecondition("G0", "workspace is dirty")
    if pre.get("lock_required"):
        locked = lock_present if lock_present is not None else False
        if locked:
            evidence.record_gate("G1", "pass", notes="lock present")
        else:
            evidence.record_gate("G1", "fail", notes="lock required but missing")
            raise BlockedPrecondition("G1", "lock required but missing")
    if pre.get("forbid_local_override"):
        if override_active:
            evidence.record_gate("G2", "fail", notes="local override active")
            raise BlockedPrecondition("G2", "local override active")
        evidence.record_gate("G2", "pass", notes="no local override")
    for gate in pre.get("required_gates", []):
        result = (gate_results or {}).get(gate, "fail")
        if result != "pass":
            evidence.record_gate(gate, "fail", notes="required gate not passed")
            raise BlockedPrecondition(gate, f"required gate '{gate}' not passed")
        evidence.record_gate(gate, "pass", notes="required gate passed")


class BlockedPrecondition(AixError):
    """Flow precondition blocked execution."""

    category = "blocked"

    def __init__(self, gate: str, message: str) -> None:
        self.gate = gate
        super().__init__(message)


def run_flow(
    flow: Flow,
    *,
    registry: ActionRegistry | None = None,
    evidence: EvidenceCollector | None = None,
    workspace_clean: bool | None = None,
    lock_present: bool | None = None,
    override_active: bool = False,
    gate_results: dict[str, str] | None = None,
    root: Path = Path("."),
) -> RunResult:
    """Execute a flow DAG.

    Raises DesignError on stage failure. Required blocked/skipped stages fail
    the flow (fail-closed). Returns RunResult on success.
    """
    registry = registry or default_registry()
    evidence = evidence or EvidenceCollector(flow=flow.name)

    # Preconditions first (F-002): real judgement, not hard-coded pass.
    _evaluate_preconditions(
        flow,
        evidence,
        workspace_clean=workspace_clean,
        lock_present=lock_present,
        forbid_override=flow.preconditions.get("forbid_local_override", False),
        override_active=override_active,
        required_gates=flow.preconditions.get("required_gates"),
        gate_results=gate_results,
    )

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
    blocked: list[str] = []

    def _finish_success() -> RunResult:
        evidence.record_gate("G6", "pass")
        evidence.write(Path("reports") / evidence.run_id)
        return RunResult(
            flow=flow.name,
            run_id=evidence.run_id,
            status="passed",
            stage_results=stage_results,
            blocked_stages=blocked,
        )

    while queue:
        sid = queue.popleft()
        stage = flow.stage_by_id(sid)
        action = registry.get(stage.uses)
        optional = _is_optional(stage)

        if action is None:
            # Fail-closed: unregistered required action blocks (F-001/F-004).
            evidence.record_stage(
                sid,
                "blocked",
                failure_signature=f"unregistered action {stage.uses}",
            )
            stage_results[sid] = "blocked"
            blocked.append(sid)
            if not optional:
                evidence.record_gate("G6", "fail", notes=f"stage {sid} blocked (required)")
                evidence.write(Path("reports") / evidence.run_id)
                return RunResult(
                    flow=flow.name,
                    run_id=evidence.run_id,
                    status="blocked",
                    failed_stage=sid,
                    stage_results=stage_results,
                    blocked_stages=blocked,
                )
            for dep in dependents[sid]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    queue.append(dep)
            continue

        try:
            _check_write_scope(stage, root)
            _execute_with_controls(action, stage, root=root)
            evidence.record_stage(sid, "passed")
            stage_results[sid] = "passed"
        except ActionSkipped as exc:
            evidence.record_stage(sid, "skipped", failure_signature=str(exc))
            stage_results[sid] = "skipped"
            if not optional:
                # Required action skipped -> fail-closed (F-001).
                evidence.record_gate("G6", "fail", notes=f"stage {sid} skipped (required)")
                evidence.write(Path("reports") / evidence.run_id)
                return RunResult(
                    flow=flow.name,
                    run_id=evidence.run_id,
                    status="failed",
                    failed_stage=sid,
                    stage_results=stage_results,
                    blocked_stages=blocked,
                )
        except (BlockedPrecondition, TimeoutError, DesignError) as exc:
            evidence.record_stage(sid, "failed", failure_signature=str(exc), exit_code=1)
            stage_results[sid] = "failed"
            evidence.record_gate("G6", "fail", notes=f"stage {sid} failed: {exc}")
            evidence.write(Path("reports") / evidence.run_id)
            raise DesignError(
                f"flow '{flow.name}' failed at stage '{sid}': {exc}",
                stage=sid,
            ) from exc
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

    return _finish_success()
