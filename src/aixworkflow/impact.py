"""Impact analysis: map a changed repository to affected downstream assets.

Conservative principle (policies/dependency-policy.yaml): when the graph is
incomplete we expand coverage, never silently shrink. Unresolvable dynamic
dependencies are marked UNKNOWN.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from aixworkflow.graph import DependencyGraph
from aixworkflow.models import Manifest


@dataclass
class ImpactResult:
    repository: str
    paths: list[str]
    direct: list[str]
    transitive: list[str]
    required_gates: list[str]
    recommended_gates: list[str]
    unknown_dependencies: list[str] = field(default_factory=list)


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

    # map repo ids to their gates by type (best-effort baseline)
    gate_map: dict[str, str] = {
        "hw-interface": "hwif-schema",
        "vip": "axi-vip-unit",
        "cbb": "cbb-unit",
        "ip": "ip-smoke",
    }
    required = []
    recommended = []
    for node in direct:
        repo = manifest.repo_by_id(node)
        required.append(gate_map.get(repo.type, f"{node}-smoke"))
    for node in sorted(downstream - set(direct)):
        repo = manifest.repo_by_id(node)
        recommended.append(gate_map.get(repo.type, f"{node}-regression"))

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
