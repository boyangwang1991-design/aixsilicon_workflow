"""Repository dependency graph: DAG validation, cycle detection, topo sort."""

from __future__ import annotations

from collections import defaultdict, deque

from aixworkflow.errors import ManifestError
from aixworkflow.models import Repository


class DependencyGraph:
    """Directed graph over repository logical ids.

    By default edges are built from the product dependency category
    (`Repository.depends_on`), which is the legacy alias. Pass `dep_type` to
    build the graph for a different typed category (ADR-0007).
    """

    def __init__(
        self,
        repositories: list[Repository],
        *,
        dep_type: str = "product",
    ) -> None:
        self.nodes: set[str] = {r.id for r in repositories}
        # edges: dependency -> dependent (downstream of its dependency)
        self.edges: dict[str, set[str]] = defaultdict(set)
        for repo in repositories:
            deps = repo.depends_on if dep_type == "product" else repo.dependencies.get(dep_type, ())
            for dep in deps:
                if dep not in self.nodes:
                    raise ManifestError(
                        f"repository '{repo.id}' has {dep_type} dependency on unknown id '{dep}'"
                    )
                self.edges[dep].add(repo.id)

    @classmethod
    def typed(
        cls,
        repositories: list[Repository],
        dep_type: str,
    ) -> DependencyGraph:
        """Build a graph for a single typed dependency category."""
        return cls(repositories, dep_type=dep_type)

    def adjacency(self) -> dict[str, list[str]]:
        """dependency -> [dependents] sorted, for stable output."""
        return {k: sorted(v) for k, v in self.edges.items()}

    def find_cycles(self) -> list[list[str]]:
        """Return all elementary cycles as node-id lists (minimal detection)."""
        cycles: list[list[str]] = []
        visited: dict[str, int] = {}  # 0=visiting, 1=done
        stack: list[str] = []

        def dfs(node: str, path: list[str]) -> None:
            visited[node] = 0
            stack.append(node)
            for nxt in sorted(self.edges.get(node, ())):
                if nxt not in visited:
                    dfs(nxt, path)
                elif visited[nxt] == 0:
                    start = path.index(nxt) if nxt in path else 0
                    cycle = path[start:] + [nxt]
                    if cycle not in cycles:
                        cycles.append(cycle)
            stack.pop()
            visited[node] = 1

        for node in sorted(self.nodes):
            if node not in visited:
                dfs(node, [])
        return cycles

    def ensure_acyclic(self) -> None:
        cycles = self.find_cycles()
        if cycles:
            desc = "; ".join(" -> ".join(c) for c in cycles)
            raise ManifestError(f"dependency DAG contains cycle(s): {desc}")

    def topological_order(self) -> list[str]:
        """Return repo ids in dependency-first topological order (Kahn)."""
        self.ensure_acyclic()
        indegree: dict[str, int] = {n: 0 for n in self.nodes}
        for node in self.nodes:
            for dep in self.edges[node]:
                indegree[dep] += 1
        queue: deque[str] = deque(sorted(n for n in self.nodes if indegree[n] == 0))
        order: list[str] = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for dep in sorted(self.edges[node]):
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    queue.append(dep)
        return order

    def dependents_of(self, repo_id: str) -> list[str]:
        """Direct dependents of a repo (downstream consumers)."""
        return sorted(self.edges.get(repo_id, ()))

    def transitive_closure(self, repo_id: str) -> set[str]:
        """All nodes reachable from repo_id (downstream impact set)."""
        seen: set[str] = set()
        stack = [repo_id]
        while stack:
            node = stack.pop()
            for nxt in self.edges.get(node, ()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen
