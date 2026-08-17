"""Data models for the aix workspace: manifest, repository, lock, resolution.

These are plain immutable-ish dataclasses populated from validated YAML.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aixworkflow.errors import ManifestError
from aixworkflow.yamlutil import dump_yaml

MANIFEST_SCHEMA_VERSION = "aix.workspace/v1"
LOCK_SCHEMA_VERSION = "aix.workspace-lock/v1"


@dataclass(frozen=True)
class WorkspaceSpec:
    name: str
    default_profile: str
    repos_root: str
    generated_root: str
    lock_root: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WorkspaceSpec:
        return cls(
            name=str(data.get("name", "aixsilicon")),
            default_profile=str(data.get("default_profile", "minimal")),
            repos_root=str(data.get("repos_root", "repos")),
            generated_root=str(data.get("generated_root", ".aix/generated")),
            lock_root=str(data.get("lock_root", ".aix")),
        )


@dataclass(frozen=True)
class CheckoutPolicy:
    shallow: bool = False
    lfs: bool = False
    sparse_paths: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CheckoutPolicy:
        data = data or {}
        return cls(
            shallow=bool(data.get("shallow", False)),
            lfs=bool(data.get("lfs", False)),
            sparse_paths=tuple(str(p) for p in data.get("sparse_paths", [])),
        )


# Typed dependency categories (ADR-0007 / target-design §5).
DEPENDENCY_TYPES = ("product", "verification", "tooling", "discovery", "context")


def _parse_dependencies(data: dict[str, Any]) -> dict[str, tuple[str, ...]]:
    """Parse typed dependencies, applying the legacy `depends_on` equivalence.

    `depends_on` is treated as `dependencies.product` during the migration
    window (ADR-0007 REV-2); explicit typed entries take precedence.
    """
    deps: dict[str, tuple[str, ...]] = {
        t: tuple(str(d) for d in data.get("dependencies", {}).get(t, [])) for t in DEPENDENCY_TYPES
    }
    legacy = tuple(str(d) for d in data.get("depends_on", []))
    # product = explicit dependencies.product if provided, else legacy depends_on
    if data.get("dependencies", {}).get("product") is None and legacy:
        deps["product"] = legacy
    return deps


@dataclass(frozen=True)
class Repository:
    id: str
    type: str
    path: str
    remote_name: str
    repo: str
    revision: dict[str, str]
    groups: tuple[str, ...]
    required: bool
    visibility: str
    owner: str
    depends_on: tuple[str, ...]
    # typed dependency categories; default keeps direct construction compatible
    # (legacy callers that only set `depends_on`).
    dependencies: dict[str, tuple[str, ...]] = field(default_factory=dict)
    fusesoc_roots: tuple[str, ...] = ()
    exports: tuple[str, ...] = ()
    checkout: CheckoutPolicy = field(default_factory=CheckoutPolicy)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Repository:
        dependencies = _parse_dependencies(data)
        return cls(
            id=str(data["id"]),
            type=str(data["type"]),
            path=str(data["path"]),
            remote_name=str(data["remote"]),
            repo=str(data["repo"]),
            revision=dict(data.get("revision", {})),
            groups=tuple(str(g) for g in data.get("groups", [])),
            required=bool(data.get("required", True)),
            visibility=str(data.get("visibility", "public")),
            owner=str(data.get("owner", "")),
            # depends_on is the product-only view (legacy alias).
            depends_on=dependencies["product"],
            dependencies=dependencies,
            fusesoc_roots=tuple(str(r) for r in data.get("fusesoc_roots", [])),
            exports=tuple(str(e) for e in data.get("exports", [])),
            checkout=CheckoutPolicy.from_dict(data.get("checkout")),
        )

    def dependency_ids(self, dep_type: str) -> tuple[str, ...]:
        """Repository ids for a single dependency category (empty when unset)."""
        return self.dependencies.get(dep_type, ())

    def remote_url(self, remotes: dict[str, dict[str, str]]) -> str:
        """Build the canonical URL from the approved remote allowlist."""
        if self.remote_name not in remotes:
            raise ManifestError(f"repository '{self.id}': unknown remote '{self.remote_name}'")
        base = remotes[self.remote_name]["base_url"]
        return f"{base.rstrip('/')}/{self.repo}"

    def resolved_revision(self, override_revision: dict[str, str] | None = None) -> dict[str, str]:
        if override_revision:
            return {**self.revision, **override_revision}
        return dict(self.revision)


@dataclass(frozen=True)
class Profile:
    """Profile selecting the exact workspace repository set (ADR-0007).

    `include_repositories` is the exact set. `optional_repositories` are
    optional additions (never required). `include_groups` is the legacy
    group-based selector, kept for backward compatibility; when
    `include_repositories` is set it takes precedence (REV-2).
    """

    name: str
    include_groups: tuple[str, ...] = ()
    include_repositories: tuple[str, ...] = ()
    optional_repositories: tuple[str, ...] = ()

    @property
    def exact(self) -> bool:
        """True when the profile uses the exact repository set."""
        return bool(self.include_repositories)

    def includes(self, repo: Repository) -> bool:
        if self.exact:
            return repo.id in self.include_repositories
        if "*" in self.include_groups:
            return True
        return bool(set(self.include_groups) & set(repo.groups))

    def is_optional(self, repo_id: str) -> bool:
        return repo_id in self.optional_repositories


@dataclass
class Manifest:
    source_path: Path
    workspace: WorkspaceSpec
    remotes: dict[str, dict[str, str]]
    repositories: list[Repository]
    profiles: dict[str, Profile]
    raw_doc: dict[str, Any] = field(default_factory=dict, repr=False)

    def repo_by_id(self, repo_id: str) -> Repository:
        for repo in self.repositories:
            if repo.id == repo_id:
                return repo
        raise ManifestError(f"unknown repository id: {repo_id}")

    def profile(self, name: str) -> Profile:
        if name not in self.profiles:
            raise ManifestError(f"unknown profile '{name}'; available: {sorted(self.profiles)}")
        return self.profiles[name]

    def enabled_repositories(self, profile: Profile) -> list[Repository]:
        return [r for r in self.repositories if profile.includes(r)]

    def required_repositories(self, profile: Profile) -> list[Repository]:
        """Required repos = enabled minus optional additions (ADR-0007)."""
        return [
            r
            for r in self.enabled_repositories(profile)
            if r.required and not profile.is_optional(r.id)
        ]

    def digest(self) -> str:
        """Canonical sha256 digest of the raw manifest document."""
        canonical = dump_yaml(self.raw_doc)
        return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
