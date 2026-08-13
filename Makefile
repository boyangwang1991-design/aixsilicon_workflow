# AIXSILICON Workflow — 统一任务入口
# 用法: make <target>

PYTHON ?= .venv/bin/python
UV     ?= uv

.PHONY: install test lint format check coverage schema clean help

help:
	@echo "Targets:"
	@echo "  install    create .venv and install package with dev deps"
	@echo "  test       run unit + integration tests"
	@echo "  lint       ruff lint (src/tests/scripts)"
	@echo "  format     ruff format check"
	@echo "  check      lint + test + schema-sync --check"
	@echo "  coverage   pytest with coverage report"
	@echo "  schema     sync packaged schemas from schemas/"
	@echo "  clean      remove build/cache/.pytest_cache"

install:
	$(UV) venv .venv --python 3.12
	$(UV) pip install --python $(PYTHON) -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests scripts

format:
	$(PYTHON) -m ruff format --check src tests scripts

schema:
	$(PYTHON) scripts/sync_schemas.py

schema-check:
	$(PYTHON) scripts/sync_schemas.py --check

check: lint schema-check test
	@echo "check: all passed"

coverage:
	$(PYTHON) -m pytest --cov=aixworkflow --cov-report=term-missing

clean:
	rm -rf build cache .pytest_cache .mypy_cache .ruff_cache
	$(PYTHON) -m aixworkflow.cli wf clean
