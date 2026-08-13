"""Unit tests: CLI package structure, registry and args (post-refactor)."""

from __future__ import annotations

from aixworkflow.cli import registry
from aixworkflow.cli.args import build_parser


def test_registry_registers_domains():
    registry.register_all()
    for key in [
        "wf.init",
        "wf.sync",
        "wf.status",
        "wf.doctor",
        "wf.lock",
        "wf.diff",
        "wf.graph",
        "wf.fusesoc",
        "wf.clean",
        "wf.run",
        "wf.test",
        "wf.foreach",
        "repo.status",
        "repo.shell",
        "repo.branch",
        "repo.commit",
        "repo.push",
        "repo.diff",
        "bundle.create",
        "bundle.validate",
        "bundle.status",
        "release.prepare",
    ]:
        assert registry.get_handler(*key.split(".", 1)) is not None, f"missing handler {key}"


def test_parser_accepts_wf_commands():
    parser = build_parser()
    ns = parser.parse_args(["wf", "lock", "--no-fetch", "-o", "out.yaml", "--profile", "release"])
    assert ns.domain == "wf"
    assert ns.command == "lock"
    assert ns.no_fetch is True
    assert ns.output == "out.yaml"
    assert ns.profile == "release"


def test_parser_accepts_run():
    parser = build_parser()
    ns = parser.parse_args(["wf", "run", "ip-verification"])
    assert ns.command == "run"
    assert ns.flow == "ip-verification"


def test_parser_accepts_bundle_validate():
    parser = build_parser()
    ns = parser.parse_args(["bundle", "validate", "CHG-2026-0042"])
    assert ns.domain == "bundle"
    assert ns.command == "validate"
    assert ns.bundle_id == "CHG-2026-0042"


def test_parser_requires_domain():
    parser = build_parser()
    try:
        parser.parse_args([])
        raise AssertionError("expected SystemExit for missing domain")
    except SystemExit:
        pass
