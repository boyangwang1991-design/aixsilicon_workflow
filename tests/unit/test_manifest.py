"""Unit tests: manifest loading, extends, overrides, schema validation."""

from __future__ import annotations

import pytest

from aixworkflow.errors import ManifestError
from aixworkflow.manifest import load_manifest, load_override
from aixworkflow.models import Manifest
from aixworkflow.yamlutil import dump_yaml


def test_load_minimal_manifest(write_manifest, tmp_path):
    path = write_manifest()
    manifest, profile, override = load_manifest(path)
    assert isinstance(manifest, Manifest)
    assert manifest.workspace.name == "test"
    assert profile == "minimal"
    assert override.source_path is None
    assert {r.id for r in manifest.repositories} == {"hwif", "vip"}


def test_profile_selection(write_manifest, tmp_path):
    path = write_manifest()
    doc = path.read_text(encoding="utf-8")
    # add an ip repo and an ip-dev profile
    doc += dump_yaml(
        {
            "repositories": [
                {
                    "id": "ip",
                    "type": "ip",
                    "path": "repos/aixsilicon_ip_repo",
                    "remote": "origin",
                    "repo": "ip_repo.git",
                    "revision": {"branch": "main"},
                    "groups": ["ip"],
                    "required": True,
                    "owner": "test",
                }
            ],
            "profiles": {"ip-dev": {"include_groups": ["base", "ip"]}},
        }
    )
    # instead rebuild cleanly to avoid YAML concatenation issues
    import yaml

    base = yaml.safe_load(path.read_text(encoding="utf-8"))
    base["repositories"].append(
        {
            "id": "ip",
            "type": "ip",
            "path": "repos/aixsilicon_ip_repo",
            "remote": "origin",
            "repo": "ip_repo.git",
            "revision": {"branch": "main"},
            "groups": ["ip"],
            "required": True,
            "owner": "test",
        }
    )
    base["profiles"]["ip-dev"] = {"include_groups": ["base", "ip"]}
    path.write_text(dump_yaml(base), encoding="utf-8")

    manifest, profile, _ = load_manifest(path, profile_name="ip-dev")
    assert profile == "ip-dev"
    assert {r.id for r in manifest.enabled_repositories(manifest.profile("ip-dev"))} == {"hwif", "vip", "ip"}


def test_unknown_profile_rejected(write_manifest):
    path = write_manifest()
    with pytest.raises(ManifestError):
        load_manifest(path, profile_name="nope")


def test_extends_resolution(tmp_path, minimal_manifest_doc):
    base = tmp_path / "manifests" / "default.yaml"
    base.parent.mkdir(parents=True)
    base.write_text(dump_yaml(minimal_manifest_doc), encoding="utf-8")
    child = tmp_path / "manifests" / "ip-dev.yaml"
    child.write_text(
        dump_yaml(
            {
                "schema_version": "aix.workspace/v1",
                "extends": "default.yaml",
                "workspace": {"name": "test", "default_profile": "ip-dev"},
                "profiles": {"ip-dev": {"include_groups": ["base"]}},
            }
        ),
        encoding="utf-8",
    )
    manifest, profile, _ = load_manifest(child)
    assert profile == "ip-dev"
    # child workspace overrides base
    assert manifest.workspace.default_profile == "ip-dev"
    assert {r.id for r in manifest.repositories} == {"hwif", "vip"}


def test_extends_cycle_detected(tmp_path):
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    a.write_text(dump_yaml({"schema_version": "aix.workspace/v1", "extends": "b.yaml"}), encoding="utf-8")
    b.write_text(dump_yaml({"schema_version": "aix.workspace/v1", "extends": "a.yaml"}), encoding="utf-8")
    with pytest.raises(ManifestError):
        load_manifest(a)


def test_invalid_manifest_rejected(tmp_path, minimal_manifest_doc):
    doc = dict(minimal_manifest_doc)
    doc["schema_version"] = "wrong"
    path = tmp_path / "bad.yaml"
    path.write_text(dump_yaml(doc), encoding="utf-8")
    with pytest.raises(ManifestError):
        load_manifest(path)


def test_override_application(write_manifest, tmp_path):
    path = write_manifest()
    override_path = tmp_path / "overrides" / "local.yaml"
    override_path.parent.mkdir(parents=True)
    override_path.write_text(
        dump_yaml(
            {
                "schema_version": "aix.workspace-override/v1",
                "repositories": {"hwif": {"revision": {"branch": "feature/x"}}},
            }
        ),
        encoding="utf-8",
    )
    manifest, _, override = load_manifest(path, override_path=override_path)
    hwif = manifest.repo_by_id("hwif")
    assert hwif.resolved_revision(override.revision_for("hwif")) == {"branch": "feature/x"}


def test_override_bad_version_rejected(tmp_path):
    override_path = tmp_path / "local.yaml"
    override_path.write_text(dump_yaml({"schema_version": "nope"}), encoding="utf-8")
    with pytest.raises(ManifestError):
        load_override(override_path)
