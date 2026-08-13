"""Evidence: Run Manifest and Evidence Index generation (aix.evidence-index/v1)."""

from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aixworkflow.schema import validate
from aixworkflow.yamlutil import write_yaml

EVIDENCE_SCHEMA_VERSION = "aix.evidence-index/v1"
RUN_MANIFEST_SCHEMA_VERSION = "aix.run-manifest/v1"


def new_run_id() -> str:
    return f"run-{datetime.datetime.now(datetime.UTC):%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:8]}"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _now() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


@dataclass
class EvidenceCollector:
    run_id: str = field(default_factory=new_run_id)
    flow: str = ""
    workspace_lock: str = ""
    manifest_digest: str = ""
    correlation_id: str = ""
    random_seed: str = ""
    stages: dict[str, dict[str, Any]] = field(default_factory=dict)
    gates: dict[str, dict[str, Any]] = field(default_factory=dict)
    artifacts: list[dict[str, str]] = field(default_factory=list)
    approvals: list[dict[str, str]] = field(default_factory=list)

    def record_stage(
        self,
        stage_id: str,
        status: str,
        *,
        exit_code: int = 0,
        tool: str = "",
        log: str = "",
        failure_signature: str = "",
    ) -> None:
        self.stages[stage_id] = {
            "status": status,
            "started_at": _now(),
            "finished_at": _now(),
            "exit_code": exit_code,
            "tool": tool,
            "log": log,
            "failure_signature": failure_signature,
        }

    def record_gate(self, gate_id: str, result: str, evidence_refs: list[str] | None = None, notes: str = "") -> None:
        self.gates[gate_id] = {
            "result": result,
            "evidence_refs": evidence_refs or [],
            "notes": notes,
        }

    def add_artifact(self, path: Path, storage_ref: str = "") -> None:
        self.artifacts.append(
            {"path": str(path), "sha256": sha256_of_file(path), "storage_ref": storage_ref}
        )

    def write(self, reports_dir: Path) -> Path:
        """Write run_manifest.yaml, evidence_index.yaml and status.json; returns reports dir."""
        reports_dir.mkdir(parents=True, exist_ok=True)

        run_manifest = {
            "schema_version": RUN_MANIFEST_SCHEMA_VERSION,
            "run_id": self.run_id,
            "correlation_id": self.correlation_id,
            "flow": self.flow,
            "workspace_lock": self.workspace_lock,
            "manifest_digest": self.manifest_digest,
            "random_seed": self.random_seed,
            "stages": self.stages,
            "gates": self.gates,
            "artifacts": self.artifacts,
            "approvals": self.approvals,
        }
        evidence = {
            "schema_version": EVIDENCE_SCHEMA_VERSION,
            "run_id": self.run_id,
            "correlation_id": self.correlation_id,
            "flow": self.flow,
            "workspace_lock": self.workspace_lock,
            "manifest_digest": self.manifest_digest,
            "random_seed": self.random_seed,
            "stages": self.stages,
            "gates": self.gates,
            "artifacts": self.artifacts,
            "approvals": self.approvals,
        }
        validate(evidence, "evidence-index", source=self.run_id)

        write_yaml(reports_dir / "run_manifest.yaml", run_manifest)
        write_yaml(reports_dir / "evidence_index.yaml", evidence)
        (reports_dir / "status.json").write_text(
            json.dumps({"run_id": self.run_id, "flow": self.flow}, indent=2) + "\n",
            encoding="utf-8",
        )
        return reports_dir
