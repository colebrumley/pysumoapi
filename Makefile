.PHONY: help setup clean test lint format format-check build publish version version-bump version-set

# Author information
AUTHOR_NAME := Cole Brumley
AUTHOR_GITHUB := colebrumley
AUTHOR_EMAIL := colebrumley@users.noreply.github.com
REPO_NAME := pysumoapi
PYTHON_VERSION := 3.11

# Virtual environment activation
VENV_DIR := .venv

help: ## Show this help
	@echo "\033[1m$(REPO_NAME) - Python client for the Sumo API\033[0m"
	@echo "\033[1mAuthor: $(AUTHOR_NAME) <$(AUTHOR_EMAIL)>\033[0m"
	@echo "\033[1mGitHub: https://github.com/$(AUTHOR_GITHUB)/$(REPO_NAME)\033[0m\n"
	@echo "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Setup development environment
setup: clean .venv/bin/activate ## Setup a clean development environment (create venv and sync dependencies)

.venv/bin/activate:
	uv venv --python=$(PYTHON_VERSION) $(VENV_DIR)
	uv pip install -e ".[dev]"

# Clean build artifacts and caches
clean: ## Clean build artifacts and caches
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(VENV_DIR)

# Run tests
test: .venv/bin/activate ## Run tests
	uv run pytest tests/ --cov=pysumoapi --cov-report=xml

# Format code
format: .venv/bin/activate ## Format code with ruff
	uv run ruff format --exclude .venv .
	uv run ruff check --fix --exclude .venv .

# Check formatting
format-check: .venv/bin/activate ## Check code formatting without making changes
	uv run ruff format --check --exclude .venv .
	uv run ruff check --exclude .venv .

# Run linters
lint: .venv/bin/activate ## Run linters (ruff, mypy)
	uv run ruff check --select ALL --exclude .venv pysumoapi

# Build the package
build: .venv/bin/activate ## Build the package
	uv run python -m build

# Publish to PyPI
publish: .venv/bin/activate ## Publish to PyPI (requires PYPI_API_TOKEN)
	@if [ -z "$$PYPI_API_TOKEN" ]; then \
		echo "Error: PYPI_API_TOKEN environment variable is not set"; \
		exit 1; \
	fi
	uv run python -m build
	uv run twine check dist/*
	uv run twine upload --username __token__ --password $$PYPI_API_TOKEN dist/*

# Show current version
version: ## Show current version
	@cat pyproject.toml | grep "^version = " | cut -d'"' -f2

# Bump version
version-bump: .venv/bin/activate ## Bump version (requires TYPE=patch|minor|major)
	@if [ -z "$$TYPE" ]; then \
		echo "Error: TYPE environment variable is not set"; \
		echo "Usage: make version-bump TYPE=<major|minor|patch>"; \
		exit 1; \
	fi
	uv run python scripts/version.py bump --type $$TYPE

# Set version
version-set: .venv/bin/activate ## Set version (requires VERSION=x.y.z)
	@if [ -z "$$VERSION" ]; then \
		echo "Error: VERSION environment variable is not set"; \
		echo "Usage: make version-set VERSION=<x.y.z>"; \
		exit 1; \
	fi
	uv run python scripts/version.py set --version $$VERSION 