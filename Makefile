.PHONY: all clean test lint format typecheck fix check-format install-protoc install-test-deps

UV ?= uv
PYTHON ?= python3.13
SRC_DIR = src
TEST_DIR = tests

all: lint typecheck test

clean:
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache build dist *.egg-info

install-protoc:
	@which protoc >/dev/null 2>&1 || (echo "Installing protoc..." && brew install protobuf)

install-test-deps:
	$(UV) pip install -e ".[dev]" -p $(PYTHON)

test: install-protoc install-test-deps
	$(UV) run -p $(PYTHON) pytest $(TEST_DIR) -v

test-cov: install-protoc install-test-deps
	$(UV) run -p $(PYTHON) --with pytest-cov --with '.[test]' pytest $(TEST_DIR) -v --cov=src/proto_to_mcp

lint:
	$(UV) run -p $(PYTHON) ruff check $(SRC_DIR) $(TEST_DIR)

format:
	$(UV) run -p $(PYTHON) ruff format $(SRC_DIR) $(TEST_DIR)

check-format:
	$(UV) run -p $(PYTHON) ruff format --check $(SRC_DIR) $(TEST_DIR)

typecheck:
	$(UV) run -p $(PYTHON) mypy $(SRC_DIR) $(TEST_DIR)

fix:
	$(UV) run -p $(PYTHON) ruff check --fix $(SRC_DIR) $(TEST_DIR)
	$(UV) run -p $(PYTHON) ruff format $(SRC_DIR) $(TEST_DIR)

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

install-uv-dev:
	$(UV) pip install -e ".[dev]" -p $(PYTHON)

install:
	$(UV) pip install -e "." -p $(PYTHON)
