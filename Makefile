.PHONY: install test lint clean pdf check

install:
	uv sync --dev

test:
	uv run pytest tests/unit tests/integration --cov=src --cov-report=term-missing

lint:
	uv run ruff check src tests scripts
	uv run python scripts/check_file_lines.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete 2>/dev/null; true
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage

pdf:
	cd latex && make

check: lint test
