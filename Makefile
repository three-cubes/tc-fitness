.PHONY: prepare check

prepare:
	uv lock
	uv sync --locked --all-extras --all-groups
	uv run --no-sync ruff check --fix src tests
	uv run --no-sync ruff format src tests

check: prepare
	uv run --no-sync tc-fitness run
