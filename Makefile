.PHONY: prepare check

prepare:
	uv run ruff check --fix src tests
	uv run ruff format src tests
	uv lock

check: prepare
	uv run tc-fitness run
