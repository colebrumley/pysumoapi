.PHONY: help install dev clean test lint format build publish docs version version-bump version-set release

# Author information
AUTHOR_NAME := Cole Brumley
AUTHOR_GITHUB := colebrumley
AUTHOR_EMAIL := colebrumley@users.noreply.github.com
REPO_NAME := pysumoapi

help: ## Show this help
	@echo "\033[1m$(REPO_NAME) - Python client for the Sumo API\033[0m"
	@echo "\033[1mAuthor: $(AUTHOR_NAME) <$(AUTHOR_EMAIL)>\033[0m"
	@echo "\033[1mGitHub: https://github.com/$(AUTHOR_GITHUB)/$(REPO_NAME)\033[0m\n"
	@echo "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Install the package in development mode
install: ## Install the package in development mode
	uv pip install -e .

# Install development dependencies
dev: ## Install development dependencies
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

# Run tests
test: ## Run tests
	uv run pytest tests/ --cov=pysumoapi --cov-report=xml

# Run linters
lint: ## Run linters (ruff, mypy)
	uv run ruff check .
	uv run mypy src/pysumoapi

# Format code
format: ## Format code with ruff
	uv run ruff format .

# Build the package
build: ## Build the package
	uv run python -m build

# Publish to PyPI
publish: ## Publish to PyPI (requires PYPI_API_TOKEN)
	@if [ -z "$$PYPI_API_TOKEN" ]; then \
		echo "Error: PYPI_API_TOKEN environment variable is not set"; \
		exit 1; \
	fi
	uv run python -m build
	uv run twine check dist/*
	uv run twine upload --username __token__ --password $$PYPI_API_TOKEN dist/*

# Build documentation (placeholder - implement when docs are added)
docs: ## Build documentation (placeholder - implement when docs are added)
	@echo "Documentation building not implemented yet"
	@echo "Consider using Sphinx or MkDocs for documentation"

# Show current version
version: ## Show current version
	uv run python scripts/version.py show

# Bump version
version-bump: ## Bump version (requires TYPE=patch|minor|major)
	@if [ -z "$$TYPE" ]; then \
		echo "Error: TYPE environment variable is not set"; \
		echo "Usage: make version-bump TYPE=<major|minor|patch>"; \
		exit 1; \
	fi
	uv run python scripts/version.py bump --type $$TYPE

# Set version
version-set: ## Set version (requires VERSION=x.y.z)
	@if [ -z "$$VERSION" ]; then \
		echo "Error: VERSION environment variable is not set"; \
		echo "Usage: make version-set VERSION=<x.y.z>"; \
		exit 1; \
	fi
	uv run python scripts/version.py set --version $$VERSION

# Create a new release
release: ## Create a new release (requires TYPE=patch|minor|major)
	@if [ -z "$$TYPE" ]; then \
		echo "Error: TYPE environment variable is not set"; \
		echo "Usage: make release TYPE=<patch|minor|major>"; \
		exit 1; \
	fi
	uv run python scripts/release.py $$TYPE 