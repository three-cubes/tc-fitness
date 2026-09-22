.PHONY: sync prepare assert-clean check-static check smoke

TC_FITNESS_BASE_REF ?= refs/remotes/origin/main

sync:
	uv sync --locked --group dev

prepare:
	uv run ruff check --fix src tests
	uv run ruff format src tests
	uv lock

assert-clean:
	@status="$$(git status --porcelain --untracked-files=all)"; \
	if [ -n "$$status" ]; then \
		echo "evaluation withheld: commit or remove every working-tree change" >&2; \
		git status --short >&2; \
		exit 1; \
	fi

check-static: assert-clean
	uv run --no-sync tc-fitness run

check:
	$(MAKE) prepare
	$(MAKE) check-static
	@base="$${TC_FITNESS_BASE_COMMIT:-$$(git merge-base "$(TC_FITNESS_BASE_REF)" HEAD)}"; \
	candidate="$$(git rev-parse HEAD)"; \
	if [ -z "$$base" ]; then \
		echo "coverage assurance requires TC_FITNESS_BASE_COMMIT or $(TC_FITNESS_BASE_REF)" >&2; \
		exit 2; \
	fi; \
	parent="$${TC_FITNESS_EVIDENCE_ROOT:-$$(mktemp -d "$${TMPDIR:-/tmp}/tc-fitness-check.XXXXXX")}"; \
	evidence="$${TC_FITNESS_EVIDENCE_DIR:-$$parent/coverage}"; \
	case "$$evidence" in /*) ;; *) echo "coverage evidence directory must be absolute" >&2; exit 2;; esac; \
	echo "coverage evidence: $$evidence"; \
	uv run --no-sync tc-fitness assure-coverage \
		--base-commit "$$base" \
		--candidate-commit "$$candidate" \
		--evidence-dir "$$evidence"

smoke: prepare
	@echo "non-admissible staged smoke: no coverage transaction is produced"
	uv run --no-sync tc-fitness run --staged
