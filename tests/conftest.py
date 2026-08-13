"""Shared pytest fixtures: temporary git repos and workspace manifests."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from aixworkflow.yamlutil import dump_yaml


def _git(*args: str, cwd: Path) -> None:
    subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def make_git_repo(tmp_path: Path):
    """Factory that creates a bare git repo (usable as a clone remote)."""

    def _make(name: str, files: dict[str, str] | None = None, branch: str = "main") -> Path:
        # bare repos use a `.git` suffix so they can be referenced by manifest URLs
        repo = tmp_path / f"{name}.git"
        work = tmp_path / f"{name}_work"
        work.mkdir(parents=True)
        _git("init", "-b", branch, cwd=work)
        _git("config", "user.email", "test@aixsilicon.dev", cwd=work)
        _git("config", "user.name", "Test", cwd=work)
        for path, content in (files or {}).items():
            target = work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        _git("add", "-A", cwd=work)
        _git("commit", "-m", "initial", cwd=work)
        _git("clone", "--bare", str(work), str(repo), cwd=tmp_path)
        return repo

    return _make


@pytest.fixture
def minimal_manifest_doc(tmp_path: Path) -> dict:
    """A minimal but valid manifest document (2 repos, DAG)."""
    return {
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
                "repo": "vip_repo.git",
                "revision": {"branch": "main"},
                "groups": ["base"],
                "depends_on": ["hwif"],
                "required": True,
                "owner": "test",
            },
        ],
        "profiles": {"minimal": {"include_groups": ["base"]}},
    }


@pytest.fixture
def write_manifest(tmp_path: Path, minimal_manifest_doc: dict):
    """Write the minimal manifest to a path and return it."""

    def _write(doc: dict | None = None) -> Path:
        path = tmp_path / "manifests" / "default.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(dump_yaml(doc or minimal_manifest_doc), encoding="utf-8")
        return path

    return _write
