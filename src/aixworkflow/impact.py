"""Impact analysis: map a changed repository to affected downstream assets.

Conservative principle (policies/dependency-policy.yaml): when the graph is
incomplete we expand coverage, never silently shrink. Unresolvable dynamic
dependencies are marked UNKNOWN.

The repo-type → gate mapping is loaded from `policies/dependency-policy.yaml`
(`gate_map:`), so policy changes do not require code edits.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from pathlib import Path

from aixworkflow.graph import DependencyGraph
from aixworkflow.models import Manifest

# Fallback mapping used only when the policy file is unreadable (e.g. tests in
# an isolated cwd). The authoritative source is policies/dependency-policy.yaml.
_DEFAULT_GATES: dict[str, str] = {
    "hw-interface": "hwif-schema",
    "vip": "axi-vip-unit",
    "cbb": "cbb-unit",
    "ip": "ip-smoke",
    "dv-common": "dv-common-unit",
    "tool": "tool-contract",
    "soc-integration": "soc-connect-check",
}


@dataclass
class ImpactResult:
    repository: str
    paths: list[str]
    direct: list[str]
    transitive: list[str]
    required_gates: list[str]
    recommended_gates: list[str]
    unknown_dependencies: list[str] = field(default_factory=list)


@functools.lru_cache(maxsize=1)
def _gate_map() -> dict[str, str]:
    """Load the repo-type → gate mapping from the dependency policy."""
    try:
        from aixworkflow.yamlutil import load_yaml

        policy = load_yaml(Path("policies") / "dependency-policy.yaml")
        raw = policy.get("gate_map") or {}
        return {str(k): str(v) for k, v in raw.items()}
    except Exception:  # noqa: BLE001 - fall back to defaults
        return dict(_DEFAULT_GATES)


def analyze_impact(
    manifest: Manifest,
    graph: DependencyGraph,
    *,
    repo_id: str,
    changed_paths: list[str] | None = None,
) -> ImpactResult:
    """Compute the downstream impact set of `repo_id`."""
    downstream = graph.transitive_closure(repo_id)
    direct = graph.dependents_of(repo_id)
    gates = _gate_map()

    required = []
    recommended = []
    for node in direct:
        repo = manifest.repo_by_id(node)
        required.append(gates.get(repo.type, f"{node}-smoke"))
    for node in sorted(downstream - set(direct)):
        repo = manifest.repo_by_id(node)
        recommended.append(gates.get(repo.type, f"{node}-regression"))

    unknown: list[str] = []
    if changed_paths is None:
        # Paths unknown -> expand coverage conservatively.
        unknown.append(f"{repo_id}:changed-paths-unknown")

    return ImpactResult(
        repository=repo_id,
        paths=changed_paths or ["<unknown>"],
        direct=direct,
        transitive=sorted(downstream - set(direct)),
        required_gates=required,
        recommended_gates=recommended,
        unknown_dependencies=unknown,
    )
