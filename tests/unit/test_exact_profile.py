"""WF-002: exact Profile + typed dependencies (ADR-0007).

Covers:
- include_repositories exact set (with optional_repositories)
- legacy include_groups fallback (backward compatibility)
- include_repositories precedence over include_groups (REV-2)
- typed dependencies parsing (product/verification/tooling/discovery/context)
- depends_on == dependencies.product legacy equivalence
- typed DependencyGraph (DAG validation, closure per category)
- negative: unknown repo id in include_repositories, unknown dep id
"""

from __future__ import annotations

import pytest

from aixworkflow.errors import ManifestError
from aixworkflow.graph import DependencyGraph
from aixworkflow.manifest import load_manifest
from aixworkflow.models import Profile, Repository
from aixworkflow.yamlutil import dump_yaml


def _repo(
    repo_id: str,
    *,
    groups: tuple[str, ...] = (),
    depends_on: list[str] | None = None,
    dependencies: dict[str, list[str]] | None = None,
) -> Repository:
    """Build a Repository through from_dict so typed-dep parsing is exercised."""
    data: dict = {
        "id": repo_id,
        "type": "ip",
        "path": f"repos/{repo_id}",
        "remote": "origin",
        "repo": f"{repo_id}.git",
        "revision": {"branch": "main"},
        "required": True,
        "owner": "test",
    }
    if groups:
        data["groups"] = list(groups)
    if depends_on is not None:
        data["depends_on"] = list(depends_on)
    if dependencies:
        data["dependencies"] = {k: list(v) for k, v in dependencies.items()}
    return Repository.from_dict(data)


def _profile(name: str, **kw) -> Profile:
    return Profile(name=name, **kw)


# --- exact Profile set --------------------------------------------------------


def test_exact_profile_uses_include_repositories():
    repos = [_repo("a", groups=("base",)), _repo("b", groups=("base",))]
    profile = _profile("min", include_repositories=("a",))
    assert [r.id for r in repos if profile.includes(r)] == ["a"]


def test_optional_repositories_are_not_required():
    repos = [_repo("a"), _repo("b")]
    profile = _profile(
        "dev",
        include_repositories=("a", "b"),
        optional_repositories=("b",),
    )
    enabled = [r for r in repos if profile.includes(r)]
    required = [r for r in enabled if r.required and not profile.is_optional(r.id)]
    assert {r.id for r in enabled} == {"a", "b"}
    assert {r.id for r in required} == {"a"}


def test_legacy_include_groups_still_works():
    repos = [_repo("a", groups=("base",)), _repo("b", groups=("dv",))]
    profile = _profile("min", include_groups=("base",))
    assert [r.id for r in repos if profile.includes(r)] == ["a"]


def test_include_repositories_takes_precedence_over_groups():
    # both fields present -> include_repositories wins (ADR-0007 REV-2)
    repos = [_repo("a", groups=("base",)), _repo("b", groups=("base",))]
    profile = _profile(
        "dev",
        include_groups=("base",),
        include_repositories=("a",),
    )
    assert profile.exact
    assert [r.id for r in repos if profile.includes(r)] == ["a"]


def test_exact_profile_unknown_repo_id_skipped():
    # a repo id listed but not present in the manifest is simply not enabled
    repos = [_repo("a")]
    profile = _profile("dev", include_repositories=("a", "ghost"))
    assert [r.id for r in repos if profile.includes(r)] == ["a"]


# --- typed dependencies parsing -----------------------------------------------


def test_depends_on_maps_to_product():
    repo = _repo("ip", depends_on=["hwif", "cbb"])
    assert repo.dependencies["product"] == ("hwif", "cbb")
    assert repo.depends_on == ("hwif", "cbb")


def test_explicit_dependencies_precedence_over_legacy():
    repo = _repo(
        "soc",
        depends_on=["hwif", "cbb", "ip"],
        dependencies={"product": ["hwif", "cbb", "ip"], "tooling": ["tools"]},
    )
    assert repo.dependencies["product"] == ("hwif", "cbb", "ip")
    assert repo.dependencies["tooling"] == ("tools",)
    assert repo.dependencies["verification"] == ()


def test_dependency_ids_helper():
    repo = _repo(
        "vip",
        dependencies={
            "product": ["hwif"],
            "verification": ["dv-common"],
            "tooling": ["tools"],
        },
    )
    assert repo.dependency_ids("product") == ("hwif",)
    assert repo.dependency_ids("verification") == ("dv-common",)
    assert repo.dependency_ids("context") == ()


# --- typed DependencyGraph ----------------------------------------------------


def test_typed_graph_builds_by_category():
    repos = [
        _repo("hwif"),
        _repo("tools"),
        _repo("ip", dependencies={"product": ["hwif"], "tooling": ["tools"]}),
    ]
    product_graph = DependencyGraph(repos, dep_type="product")
    tooling_graph = DependencyGraph(repos, dep_type="tooling")
    assert product_graph.dependents_of("hwif") == ["ip"]
    assert tooling_graph.dependents_of("tools") == ["ip"]
    assert tooling_graph.dependents_of("hwif") == []


def test_typed_closure_per_category():
    repos = [
        _repo("hwif"),
        _repo("dv-common"),
        _repo("vip", dependencies={"product": ["hwif"], "verification": ["dv-common"]}),
    ]
    product_graph = DependencyGraph(repos, dep_type="product")
    verification_graph = DependencyGraph(repos, dep_type="verification")
    assert product_graph.transitive_closure("hwif") == {"vip"}
    assert verification_graph.transitive_closure("dv-common") == {"vip"}
    # verification graph has no hwif edge
    assert verification_graph.transitive_closure("hwif") == set()


def test_typed_graph_negative_unknown_dep():
    repos = [_repo("ip", dependencies={"product": ["ghost"]})]
    with pytest.raises(ManifestError):
        DependencyGraph(repos, dep_type="product")


def test_typed_graph_cycle_detected():
    repos = [
        _repo("a", dependencies={"product": ["b"]}),
        _repo("b", dependencies={"product": ["a"]}),
    ]
    graph = DependencyGraph(repos, dep_type="product")
    assert graph.find_cycles()
    with pytest.raises(ManifestError):
        graph.ensure_acyclic()


# --- manifest-level integration ----------------------------------------------


def test_manifest_exact_profiles(write_manifest, tmp_path):
    """Manifest with include_repositories produces exact repo sets."""
    doc = {
        "schema_version": "aix.workspace/v1",
        "workspace": {
            "name": "test",
            "default_profile": "minimal",
            "repos_root": "repos",
            "generated_root": ".aix/generated",
            "lock_root": ".aix",
        },
        "remotes": {"origin": {"base_url": str(tmp_path)}},
        "repositories": [
            {
                "id": "hwif",
                "type": "hw-interface",
                "path": "repos/aixsilicon_hwif_repo",
                "remote": "origin",
                "repo": "hwif_repo.git",
                "revision": {"branch": "main"},
                "required": True,
                "owner": "test",
            },
            {
                "id": "tools",
                "type": "tool",
                "path": "repos/aixsilicon_tool_repo",
                "remote": "origin",
                "repo": "tool_repo.git",
                "revision": {"branch": "main"},
                "required": True,
                "owner": "test",
            },
            {
                "id": "ip",
                "type": "ip",
                "path": "repos/aixsilicon_ip_repo",
                "remote": "origin",
                "repo": "ip_repo.git",
                "revision": {"branch": "main"},
                "depends_on": ["hwif"],
                "required": True,
                "owner": "test",
            },
        ],
        "profiles": {
            "minimal": {"include_repositories": ["hwif", "tools"]},
            "ip-dev": {
                "include_repositories": ["hwif", "ip", "tools"],
                "optional_repositories": ["tools"],
            },
        },
    }
    path = tmp_path / "manifests" / "exact.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(doc), encoding="utf-8")

    manifest, profile, _ = load_manifest(path, profile_name="minimal")
    minimal = manifest.profile("minimal")
    assert {r.id for r in manifest.enabled_repositories(minimal)} == {"hwif", "tools"}

    manifest, profile, _ = load_manifest(path, profile_name="ip-dev")
    ipdev = manifest.profile("ip-dev")
    assert {r.id for r in manifest.required_repositories(ipdev)} == {"hwif", "ip"}
    assert ipdev.is_optional("tools")


def test_manifest_typed_dependencies_loaded(write_manifest, tmp_path):
    """depends_on and dependencies.product are both parsed from YAML."""
    doc = {
        "schema_version": "aix.workspace/v1",
        "workspace": {
            "name": "test",
            "default_profile": "minimal",
            "repos_root": "repos",
            "generated_root": ".aix/generated",
            "lock_root": ".aix",
        },
        "remotes": {"origin": {"base_url": str(tmp_path)}},
        "repositories": [
            {
                "id": "hwif",
                "type": "hw-interface",
                "path": "repos/aixsilicon_hwif_repo",
                "remote": "origin",
                "repo": "hwif_repo.git",
                "revision": {"branch": "main"},
                "required": True,
                "owner": "test",
            },
            {
                "id": "ip",
                "type": "ip",
                "path": "repos/aixsilicon_ip_repo",
                "remote": "origin",
                "repo": "ip_repo.git",
                "revision": {"branch": "main"},
                "dependencies": {
                    "product": ["hwif"],
                    "tooling": ["tools"],
                    "context": ["skills", "knowledge"],
                },
                "required": True,
                "owner": "test",
            },
        ],
        "profiles": {
            "minimal": {
                "include_groups": ["base"],
                "include_repositories": ["hwif", "ip"],
            }
        },
    }
    path = tmp_path / "manifests" / "typed.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(doc), encoding="utf-8")

    manifest, _, _ = load_manifest(path)
    ip_repo = manifest.repo_by_id("ip")
    assert ip_repo.dependencies["product"] == ("hwif",)
    assert ip_repo.dependencies["tooling"] == ("tools",)
    assert ip_repo.dependencies["context"] == ("skills", "knowledge")
