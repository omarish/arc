.PHONY: sync-keys format lint typecheck fix-all test test-cov

sync-keys:
	gsutil -m rsync -r private_keys gs://arc-keys/

format:
	black .
	ruff --fix .

lint:
	black --check .
	ruff check .
	mypy .

typecheck:
	mypy .

test:
	uv run pytest

test-cov:
	uv run pytest

fix-all: format lint

# Install development dependencies
dev-setup:
	pip install -e ".[dev]"