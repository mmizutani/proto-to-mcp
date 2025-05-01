.PHONY: all clean test lint format typecheck fix check-format install-protoc install-test-deps build

UV ?= uv
SRC_DIR = src
TEST_DIR = tests

all: lint typecheck test

clean:
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache build dist *.egg-info

install-protoc:
	@which protoc >/dev/null 2>&1 || (echo "Installing protoc..." && brew install protobuf)

install-test-deps:
	$(UV) pip install -e ".[dev]"

test: install-protoc install-test-deps
	$(UV) run pytest $(TEST_DIR) -v

test-cov: install-protoc install-test-deps
	$(UV) run --with pytest-cov --with '.[test]' pytest $(TEST_DIR) -v --cov=src/proto_to_mcp

lint:
	$(UV) run ruff check $(SRC_DIR) $(TEST_DIR)

format:
	$(UV) run ruff format $(SRC_DIR) $(TEST_DIR)

check-format:
	$(UV) run ruff format --check $(SRC_DIR) $(TEST_DIR)

typecheck:
	$(UV) run mypy $(SRC_DIR) $(TEST_DIR)

fix:
	$(UV) run ruff check --fix $(SRC_DIR) $(TEST_DIR)
	$(UV) run ruff format $(SRC_DIR) $(TEST_DIR)

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

install-uv-dev:
	$(UV) pip install -e ".[dev]"

install:
	$(UV) pip install -e "."

build:
	$(UV) build
