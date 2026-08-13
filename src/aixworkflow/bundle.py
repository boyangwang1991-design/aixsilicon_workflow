"""Change Bundle: load, validate and describe `aix.change-bundle/v1` documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aixworkflow.errors import ManifestError
from aixworkflow.schema import validate
from aixworkflow.yamlutil import load_yaml

BUNDLE_SCHEMA_VERSION = "aix.change-bundle/v1"

VALID_STATUSES = (
    "draft",
    "ready",
    "validating",
    "blocked",
    "review",
    "merge-ready",
    "merged",
    "released",
    "closed",
)


@dataclass
class BundleRepo:
    id: str
    branch: str
    base: str
    pr: int | None
    merge_order: int | None
    depends_on: list[str]

    @classmethod
    def from_dict(cls, repo_id: str, data: dict[str, Any]) -> BundleRepo:
        return cls(
            id=repo_id,
            branch=str(data["branch"]),
            base=str(data["base"]),
            pr=data.get("pr"),
            merge_order=data.get("merge_order"),
            depends_on=[str(d) for d in data.get("depends_on", [])],
        )


@dataclass
class ChangeBundle:
    id: str
    title: str
    owner: str
    status: str
    repositories: list[BundleRepo]
    validation: dict[str, Any]
    release_plan: dict[str, str]
    source_path: Path

    def repo_by_id(self, repo_id: str) -> BundleRepo:
        for repo in self.repositories:
            if repo.id == repo_id:
                return repo
        raise ManifestError(f"bundle '{self.id}': unknown repository '{repo_id}'")


def load_bundle(path: Path) -> ChangeBundle:
    doc = load_yaml(path)
    validate(doc, "change-bundle", source=str(path))
    repos = [BundleRepo.from_dict(rid, d) for rid, d in doc["repositories"].items()]
    return ChangeBundle(
        id=str(doc["id"]),
        title=str(doc["title"]),
        owner=str(doc["owner"]),
        status=str(doc["status"]),
        repositories=repos,
        validation=dict(doc.get("validation", {})),
        release_plan={str(k): str(v) for k, v in doc.get("release_plan", {}).items()},
        source_path=path,
    )


def validate_merge_order(bundle: ChangeBundle) -> list[str]:
    """Return a dependency-first merge order for the bundle repositories."""
    order: list[str] = []
    placed: set[str] = set()

    def place(repo: BundleRepo, stack: list[str]) -> None:
        if repo.id in placed:
            return
        if repo.id in stack:
            raise ManifestError(f"bundle merge dependency cycle: {' -> '.join(stack + [repo.id])}")
        for dep in repo.depends_on:
            dep_repo = bundle.repo_by_id(dep)
            place(dep_repo, stack + [repo.id])
        placed.add(repo.id)
        order.append(repo.id)

    for repo in bundle.repositories:
        place(repo, [])
    return order
