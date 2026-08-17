"""Action capability registry and preflight (ADR-0008, WF-004/TOOL-001).

Separates Flow, Action Contract and Provider:

- an Action Contract declares a stable name, its provider, version constraints,
  input/output schema, determinism, environment requirements, write scope and
  evidence requirements;
- a Provider is the real implementation (builtin, plugin, external CLI);
- preflight() evaluates every stage of a flow *before* execution and produces a
  capability matrix with one of the six ADR-0008 states:
    available / optional-unavailable / unimplemented / version-mismatch /
    environment-unavailable
- a required action that is not `available` blocks the flow (fail-closed), so a
  `blocked`/`skipped` stage can never be summarized as a pass (F-001/F-004).
"""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass, field

from aixworkflow.flow import Flow, FlowStage

# ADR-0008 capability states (single source of truth).
AVAILABLE = "available"
OPTIONAL_UNAVAILABLE = "optional-unavailable"
UNIMPLEMENTED = "unimplemented"
VERSION_MISMATCH = "version-mismatch"
ENVIRONMENT_UNAVAILABLE = "environment-unavailable"

STATES: tuple[str, ...] = (
    AVAILABLE,
    OPTIONAL_UNAVAILABLE,
    UNIMPLEMENTED,
    VERSION_MISMATCH,
    ENVIRONMENT_UNAVAILABLE,
)

# Binary names probed by `environment-unavailable` detection for external tools.
_PROBE: dict[str, tuple[str, ...]] = {
    "fusesoc": ("fusesoc",),
    "git": ("git",),
    "verilator": ("verilator",),
    "iverilog": ("iverilog",),
    "python": (sys.executable,),
}


@dataclass(frozen=True)
class ActionContract:
    """Stable metadata for an action (ADR-0008)."""

    name: str
    provider: str
    version: str
    determinism: bool = True
    environment: tuple[str, ...] = ()
    write_scope: tuple[str, ...] = ()
    evidence_required: bool = True


@dataclass
class CapabilityEntry:
    """Per-stage preflight evaluation result."""

    stage: str
    action: str
    state: str
    provider: str = ""
    version: str = ""
    detail: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "stage": self.stage,
            "action": self.action,
            "state": self.state,
            "provider": self.provider,
            "version": self.version,
            "detail": self.detail,
        }


@dataclass
class PreflightResult:
    """Preflight output: full capability matrix + blocking info."""

    flow: str
    entries: list[CapabilityEntry] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.blocked

    def matrix(self) -> list[dict[str, str]]:
        return [e.to_dict() for e in self.entries]


class CapabilityRegistry:
    """Registry of known action contracts and available providers."""

    def __init__(self) -> None:
        self._contracts: dict[str, ActionContract] = {}
        self._available: set[str] = set()
        self._enabled_env: set[str] = set()

    def register(
        self,
        name: str,
        *,
        provider: str,
        version: str = "",
        determinism: bool = True,
        environment: tuple[str, ...] = (),
        write_scope: tuple[str, ...] = (),
        evidence_required: bool = True,
        available: bool = False,
        enabled_environment: bool = True,
    ) -> None:
        """Register an action contract and its availability."""
        self._contracts[name] = ActionContract(
            name=name,
            provider=provider,
            version=version,
            determinism=determinism,
            environment=environment,
            write_scope=write_scope,
            evidence_required=evidence_required,
        )
        if available:
            self._available.add(name)
        if enabled_environment:
            self._enabled_env.add(name)

    def contracts(self) -> dict[str, ActionContract]:
        return dict(self._contracts)

    def get(self, name: str) -> ActionContract | None:
        return self._contracts.get(name)

    def _environment_ok(self, contract: ActionContract) -> bool:
        """True when the contract's required binaries are on PATH."""
        if not contract.environment:
            return True
        for binary in contract.environment:
            probes = _PROBE.get(binary, (binary,))
            if not any(shutil.which(p) for p in probes):
                return False
        return True

    def evaluate(self, stage: FlowStage, *, required: bool) -> CapabilityEntry:
        """Evaluate a single stage against the registry (ADR-0008 6 states)."""
        contract = self._contracts.get(stage.uses)
        if contract is None:
            # Unknown contract -> not implemented in this registry.
            state = UNIMPLEMENTED if required else OPTIONAL_UNAVAILABLE
            return CapabilityEntry(
                stage=stage.id,
                action=stage.uses,
                state=state,
                detail="no provider/contract registered",
            )
        if contract.name not in self._available:
            state = UNIMPLEMENTED if required else OPTIONAL_UNAVAILABLE
            return CapabilityEntry(
                stage=stage.id,
                action=stage.uses,
                state=state,
                provider=contract.provider,
                version=contract.version,
                detail="provider not available in this registry",
            )
        if not self._environment_ok(contract):
            state = ENVIRONMENT_UNAVAILABLE
            return CapabilityEntry(
                stage=stage.id,
                action=stage.uses,
                state=state,
                provider=contract.provider,
                version=contract.version,
                detail=f"missing environment: {', '.join(contract.environment)}",
            )
        if contract.name not in self._enabled_env:
            state = ENVIRONMENT_UNAVAILABLE
            return CapabilityEntry(
                stage=stage.id,
                action=stage.uses,
                state=state,
                provider=contract.provider,
                version=contract.version,
                detail="environment feature not enabled",
            )
        return CapabilityEntry(
            stage=stage.id,
            action=stage.uses,
            state=AVAILABLE,
            provider=contract.provider,
            version=contract.version,
        )

    def preflight(self, flow: Flow) -> PreflightResult:
        """Evaluate all stages of a flow; block any non-available required action.

        An action is *required* when it is not registered as optional and not a
        `skill.*` namespace (skills are always optional per ADR-0008).
        """
        result = PreflightResult(flow=flow.name)
        for stage in flow.stages:
            required = _is_required(stage)
            entry = self.evaluate(stage, required=required)
            result.entries.append(entry)
            if required and entry.state != AVAILABLE:
                result.blocked.append(stage.id)
        return result


def _is_required(stage: FlowStage) -> bool:
    """A stage is required unless it is a skill action (always optional)."""
    return not stage.uses.startswith("skill.")


def default_registry() -> CapabilityRegistry:
    """Registry reflecting the current builtin providers (see runner.actions).

    Mirrors `default_registry()` in runner.py so preflight and execution agree.
    """
    registry = CapabilityRegistry()
    registry.register(
        "workspace.resolve",
        provider="builtin",
        version="0.1.0",
        available=True,
    )
    registry.register(
        "fusesoc.target",
        provider="fusesoc",
        version="*",
        environment=("fusesoc",),
    )
    registry.register(
        "hwif.compatibility-check",
        provider="builtin+script",
        version="0.1.0",
        available=True,
    )
    registry.register("hwif.compatibility", provider="builtin+script", version="0.1.0")
    registry.register(
        "eda.regression",
        provider="external",
        version="*",
        environment=("git",),
    )
    registry.register("evidence.index", provider="builtin", version="0.1.0", available=True)
    registry.register(
        "release.package",
        provider="builtin",
        version="0.1.0",
        available=True,
    )
    # tool.* / catalog.* / soc.* / bundle.* / git.* / graph.* / impact.* /
    # flow.* / release.*(others) / eda.*(others) are intentionally not
    # registered here yet (action inventory gap, F-004).
    return registry


def probe_environment() -> dict[str, bool]:
    """Probe basic toolchain availability (doctor/preflight helper)."""
    return {
        binary: any(shutil.which(p) for p in probes)
        for binary, probes in _PROBE.items()
    }
