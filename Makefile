.PHONY: import-02-llm push-02-llm

# Импортирует проект домашнего задания в локальный репозиторий в папку 02-llm-api
import-02-llm:
	@set -e; tmpdir=$$(mktemp -d); \
	cd "$$tmpdir"; \
	git clone https://github.com/aidialogs/sber-agents.git temp-repo; \
	mkdir -p "$(PWD)/02-llm-api"; \
	cp -a temp-repo/02-llm-api/homework/project/. "$(PWD)/02-llm-api/"; \
	rm -rf "$$tmpdir"

# Коммитит и пушит изменения в удалённый репозиторий (ветка main)
push-02-llm:
	git add 02-llm-api
	git commit -m "Add 02-llm-api homework project"
	git push origin main

# Default target
.PHONY: help check

help:
	@echo "Available targets:"
	@echo "  make check     - Print environment info via Make"

check:
	@echo "MAKE_OK"
	@echo "SHELL=$$SHELL"
	@echo "PWD=$$(pwd)"
	@echo "WHOAMI=$$(whoami 2>NUL || echo unknown)"

