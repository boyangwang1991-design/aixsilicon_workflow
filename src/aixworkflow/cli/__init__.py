"""`aix` CLI package.

Keeps the `aixworkflow.cli:main` console entry point (pyproject.toml).
The package splits parsing, dispatch, context and per-domain handlers into
small modules so new commands can be added with minimal changes.
"""

from aixworkflow.cli.app import main

__all__ = ["main"]
