"""Integration tests: end-to-end workspace init/sync/lock/status against temp repos."""

from __future__ import annotations

import pytest

from aixworkflow.resolver import WORKSPACE_MODE, generate_lock
from aixworkflow.workspace import init_workspace, sync_workspace, workspace_status
from aixworkflow.yamlutil import dump_yaml


def _build_manifest(tmp_path, make_git_repo) -> None:
    """Create a full manifest pointing at two local bare repos."""
    hwif = make_git_repo("aixsilicon_hwif_repo", files={"README.md": "# hwif\n"})
    vip = make_git_repo("aixsilicon_vip_repo", files={"README.md": "# vip\n"})
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
                "repo": "aixsilicon_hwif_repo.git",
                "revision": {"branch": "main"},
                "groups": ["base"],
                "required": True,
                "owner": "test",
                "fusesoc_roots": ["."],
            },
            {
                "id": "vip",
                "type": "vip",
                "path": "repos/aixsilicon_vip_repo",
                "remote": "origin",
                "repo": "aixsilicon_vip_repo.git",
                "revision": {"branch": "main"},
                "groups": ["base"],
                "depends_on": ["hwif"],
                "required": True,
                "owner": "test",
            },
        ],
        "profiles": {"minimal": {"include_groups": ["base"]}},
    }
    manifest_dir = tmp_path / "manifests"
    manifest_dir.mkdir(exist_ok=True)
    (manifest_dir / "default.yaml").write_text(dump_yaml(doc), encoding="utf-8")
    return hwif, vip


def test_init_sync_status_lock(tmp_path, make_git_repo):
    hwif, vip = _build_manifest(tmp_path, make_git_repo)
    manifest_path = tmp_path / "manifests" / "default.yaml"

    manifest, profile, override = init_workspace(tmp_path, manifest_path, None)
    assert profile == "minimal"
    assert (tmp_path / "repos").is_dir()
    assert (tmp_path / ".aix" / "generated").is_dir()

    report = sync_workspace(tmp_path, manifest, profile, override)
    assert set(report.cloned) == {"hwif", "vip"}
    assert (tmp_path / "repos" / "aixsilicon_hwif_repo" / ".git").exists()

    # second sync: repos already exist -> fetch, no clone
    report2 = sync_workspace(tmp_path, manifest, profile, override)
    assert report2.cloned == []

    # status
    rows = workspace_status(tmp_path, manifest, profile, override)
    by_id = {r[0].id: r for r in rows}
    assert by_id["hwif"][1].present

    # lock
    result = generate_lock(manifest, profile, override, workspace_root=tmp_path, mode=WORKSPACE_MODE)
    assert len(result.repositories) == 2
    lock = result.to_lock_doc(manifest, {"profile": "unset"})
    assert lock["repositories"]["hwif"]["commit"]
    assert lock["repositories"]["vip"]["commit"] != lock["repositories"]["hwif"]["commit"]


def test_dirty_tree_skipped(tmp_path, make_git_repo):
    hwif, vip = _build_manifest(tmp_path, make_git_repo)
    manifest_path = tmp_path / "manifests" / "default.yaml"
    manifest, profile, override = init_workspace(tmp_path, manifest_path, None)
    sync_workspace(tmp_path, manifest, profile, override)

    # dirty one repo
    (tmp_path / "repos" / "aixsilicon_hwif_repo" / "scratch.txt").write_text("x", encoding="utf-8")
    report = sync_workspace(tmp_path, manifest, profile, override)
    assert "hwif" in report.skipped


def test_release_mode_rejects_dirty(tmp_path, make_git_repo):
    from aixworkflow.resolver import RELEASE_MODE

    hwif, vip = _build_manifest(tmp_path, make_git_repo)
    manifest_path = tmp_path / "manifests" / "default.yaml"
    manifest, profile, override = init_workspace(tmp_path, manifest_path, None)
    sync_workspace(tmp_path, manifest, profile, override)
    (tmp_path / "repos" / "aixsilicon_hwif_repo" / "x.txt").write_text("x", encoding="utf-8")
    with pytest.raises(Exception) as excinfo:
        generate_lock(manifest, profile, override, workspace_root=tmp_path, mode=RELEASE_MODE)
    assert "dirty" in str(excinfo.value).lower()
