.PHONY: all clean test lint format typecheck fix check-format

PYTHON ?= python
SRC_DIR = src
TEST_DIR = tests

all: lint typecheck test

clean:
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache build dist *.egg-info

test:
	$(PYTHON) -m pytest $(TEST_DIR) -v --cov=src/proto_to_mcp

lint:
	$(PYTHON) -m ruff check $(SRC_DIR) $(TEST_DIR)

format:
	$(PYTHON) -m ruff format $(SRC_DIR) $(TEST_DIR)

check-format:
	$(PYTHON) -m ruff format --check $(SRC_DIR) $(TEST_DIR)

typecheck:
	$(PYTHON) -m mypy $(SRC_DIR) $(TEST_DIR)

fix:
	$(PYTHON) -m ruff check --fix $(SRC_DIR) $(TEST_DIR)
	$(PYTHON) -m ruff format $(SRC_DIR) $(TEST_DIR)

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

install-uv-dev:
	uv pip install -e ".[dev]"
