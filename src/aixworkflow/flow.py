"""Flow definitions: load, validate and describe `aix.flow/v1` documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aixworkflow.errors import ManifestError
from aixworkflow.schema import validate
from aixworkflow.yamlutil import load_yaml

FLOW_SCHEMA_VERSION = "aix.flow/v1"

# Registered action namespaces. `uses` may only reference these; arbitrary
# shell strings are forbidden (policies/security-policy.yaml).
ALLOWED_ACTION_NAMESPACES: tuple[str, ...] = (
    "workspace.",
    "hwif.",
    "vip.",
    "cbb.",
    "ip.",
    "soc.",
    "tool.",
    "fusesoc.",
    "eda.",
    "release.",
    "evidence.",
    "impact.",
    "catalog.",
    "graph.",
    "git.",
    "bundle.",
    "flow.",
    "skill.",
)


@dataclass
class FlowStage:
    id: str
    uses: str
    needs: list[str]
    with_: dict[str, Any]
    write_scope: list[dict[str, Any]]
    timeout_seconds: int | None
    retries: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FlowStage:
        return cls(
            id=str(data["id"]),
            uses=str(data["uses"]),
            needs=[str(n) for n in data.get("needs", [])],
            with_=dict(data.get("with", {})),
            write_scope=list(data.get("write_scope", [])),
            timeout_seconds=data.get("timeout_seconds"),
            retries=int(data.get("retries", 0)),
        )


@dataclass
class Flow:
    name: str
    description: str
    inputs: list[str]
    preconditions: dict[str, Any]
    stages: list[FlowStage]
    on_failure: str
    source_path: Path

    def stage_by_id(self, stage_id: str) -> FlowStage:
        for stage in self.stages:
            if stage.id == stage_id:
                return stage
        raise ManifestError(f"flow '{self.name}': unknown stage '{stage_id}'")


def load_flow(path: Path) -> Flow:
    doc = load_yaml(path)
    validate(doc, "flow", source=str(path))
    return Flow(
        name=str(doc["name"]),
        description=str(doc.get("description", "")),
        inputs=[str(i) for i in doc.get("inputs", [])],
        preconditions=dict(doc.get("preconditions", {})),
        stages=[FlowStage.from_dict(s) for s in doc.get("stages", [])],
        on_failure=str(doc.get("on_failure", "collect_evidence_then_fail")),
        source_path=path,
    )


def assert_registered_action(uses: str) -> None:
    """Raise when a stage references an unregistered action namespace."""
    for ns in ALLOWED_ACTION_NAMESPACES:
        if uses.startswith(ns):
            return
    raise ManifestError(f"flow uses unregistered action: '{uses}'")
