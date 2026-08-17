# AIXSILICON Workflow — 统一任务入口
# 用法: make <target>
#
# Skill 集中管理架构：canonical src/tests/scripts 由私有 skill repo
# `skills/aixsilicon-workspace-management/` 统一管理；各目标先经 bootstrap.py
# 物化 skills 到 ./.roo/skills/（git 忽略），再从 ./.roo/skills/aixsilicon-workspace-management/ 运行。
# 跨平台入口（F-013 / WF-011）：Python 一律经 uv 解析到根环境。

PYTHON ?= uv run python
UV     ?= uv
BOOTSTRAP := $(PYTHON) bootstrap.py --ensure
SKILL_DIR := .roo/skills/aixsilicon-workspace-management

.PHONY: install bootstrap test lint format check coverage schema clean help

help:
	@echo "Targets:"
	@echo "  bootstrap  download skill repo + materialize skills to .roo/skills"
	@echo "  install    create .venv and install launcher (dev deps)"
	@echo "  test       run unit + integration tests (from .roo/skills)"
	@echo "  lint       ruff lint (skill src/tests/scripts)"
	@echo "  format     ruff format check"
	@echo "  check      bootstrap + lint + schema-check + test"
	@echo "  coverage   pytest with coverage report"
	@echo "  schema     sync packaged schemas from schemas/"
	@echo "  clean      remove build/cache/.pytest_cache"

bootstrap:
	$(BOOTSTRAP)

install:
	$(UV) venv .venv --python 3.12 --allow-existing
	$(UV) sync --extra dev

# 物化 skill 位于 ./.roo/skills/aixsilicon-workspace-management；用 workflow 根环境 + PYTHONPATH 执行。
export PYTHONPATH := $(SKILL_DIR)/src$(if $(findstring Windows,$(OS)),;,:)$(PYTHONPATH)
export AIX_RUNTIME_SRC := $(SKILL_DIR)/src

test: bootstrap
	$(PYTHON) -m pytest $(SKILL_DIR)/tests -q --rootdir=$(SKILL_DIR)

lint: bootstrap
	$(PYTHON) -m ruff check $(SKILL_DIR)/src $(SKILL_DIR)/tests $(SKILL_DIR)/scripts

format: bootstrap
	$(PYTHON) -m ruff format --check $(SKILL_DIR)/src $(SKILL_DIR)/tests $(SKILL_DIR)/scripts

schema: bootstrap
	$(PYTHON) $(SKILL_DIR)/scripts/sync_schemas.py --schemas-dir schemas --pkg-dir $(SKILL_DIR)/src/aixworkflow/schemas

schema-check: bootstrap
	$(PYTHON) $(SKILL_DIR)/scripts/sync_schemas.py --check --schemas-dir schemas --pkg-dir $(SKILL_DIR)/src/aixworkflow/schemas

check: lint schema-check test
	@echo "check: all passed"

coverage: bootstrap
	$(PYTHON) -m pytest $(SKILL_DIR)/tests --cov=aixworkflow --cov-report=term-missing --rootdir=$(SKILL_DIR)

clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p) for p in ('build','cache','.pytest_cache','.mypy_cache','.ruff_cache') if __import__('os').path.exists(p)]"
	$(PYTHON) bootstrap.py aix wf clean
