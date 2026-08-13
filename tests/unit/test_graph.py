"""Unit tests: dependency graph, cycles, topo sort, impact."""

from __future__ import annotations

import pytest

from aixworkflow.errors import ManifestError
from aixworkflow.graph import DependencyGraph
from aixworkflow.impact import analyze_impact
from aixworkflow.models import Repository


def _repo(repo_id: str, depends_on: list[str] | None = None, type_: str = "ip") -> Repository:
    return Repository(
        id=repo_id,
        type=type_,
        path=f"repos/{repo_id}",
        remote_name="origin",
        repo=f"{repo_id}.git",
        revision={"branch": "main"},
        groups=(),
        required=True,
        visibility="public",
        owner="test",
        depends_on=tuple(depends_on or []),
        fusesoc_roots=(),
        exports=(),
        checkout=None,  # type: ignore[arg-type]
    )


def test_acyclic_topological_order():
    repos = [
        _repo("hwif"),
        _repo("cbb", ["hwif"]),
        _repo("ip", ["hwif", "cbb"]),
        _repo("vip", ["hwif"]),
    ]
    graph = DependencyGraph(repos)
    order = graph.topological_order()
    assert order.index("hwif") < order.index("cbb")
    assert order.index("hwif") < order.index("vip")
    assert order.index("cbb") < order.index("ip")


def test_cycle_detected():
    repos = [_repo("a", ["b"]), _repo("b", ["a"])]
    graph = DependencyGraph(repos)
    assert graph.find_cycles()
    with pytest.raises(ManifestError):
        graph.ensure_acyclic()


def test_unknown_dependency_rejected():
    repos = [_repo("a", ["ghost"])]
    with pytest.raises(ManifestError):
        DependencyGraph(repos)


def test_transitive_closure():
    repos = [
        _repo("hwif"),
        _repo("vip", ["hwif"]),
        _repo("ip", ["hwif", "vip"]),
    ]
    graph = DependencyGraph(repos)
    assert graph.transitive_closure("hwif") == {"vip", "ip"}


def test_impact_analysis(write_manifest, minimal_manifest_doc):
    repos = [_repo("hwif"), _repo("vip", ["hwif"], "vip"), _repo("ip", ["hwif", "vip"])]
    by_id = {r.id: r for r in repos}
    manifest = type("M", (), {})()
    manifest.repo_by_id = by_id.__getitem__
    manifest.repositories = repos
    graph = DependencyGraph(repos)
    result = analyze_impact(
        manifest,  # type: ignore[arg-type]
        graph,
        repo_id="hwif",
        changed_paths=["interfaces/axi/contract.yaml"],
    )
    # ip and vip both directly depend on hwif
    assert result.direct == ["ip", "vip"]
    assert result.transitive == []
    assert result.required_gates == ["ip-smoke", "axi-vip-unit"]
