# PySumoAPI

[![PyPI version](https://badge.fury.io/py/pysumoapi.svg)](https://badge.fury.io/py/pysumoapi)
[![Python Versions](https://img.shields.io/pypi/pyversions/pysumoapi.svg)](https://pypi.org/project/pysumoapi/)
[![License](https://img.shields.io/github/license/colebrumley/pysumoapi.svg)](https://github.com/colebrumley/pysumoapi/blob/main/LICENSE)
[![Tests](https://github.com/colebrumley/pysumoapi/actions/workflows/test.yml/badge.svg)](https://github.com/colebrumley/pysumoapi/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/colebrumley/pysumoapi/branch/main/graph/badge.svg)](https://codecov.io/gh/colebrumley/pysumoapi)

A Python client library for the [Sumo API](https://sumo-api.com), providing easy access to sumo wrestling data including rikishi information, statistics, shikona history, measurements, and rank history.

## Features

- Asynchronous API client using `httpx`
- Strongly typed data models using `pydantic`
- Comprehensive error handling
- Command-line interface for quick data access
- Detailed examples demonstrating API usage

## Installation

```bash
# Using pip
pip install pysumoapi

# Using uv (recommended)
uv pip install pysumoapi
```

## Quick Start

```python
import asyncio
from pysumoapi.client import SumoClient

async def main():
    async with SumoClient() as client:
        # Get rikishi information
        rikishi = await client.get_rikishi(1511)
        print(f"Name: {rikishi.shikona_en}")
        
        # Get rikishi statistics
        stats = await client.get_rikishi_stats(1511)
        print(f"Total matches: {stats.total_matches}")
        
        # Get shikona history
        shikonas = await client.get_shikonas(rikishi_id=1511, sort_order="asc")
        for shikona in shikonas:
            print(f"Basho: {shikona.basho_id}, Shikona: {shikona.shikona_en}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Command-Line Interface

PySumoAPI includes a command-line interface for quick data access:

```bash
# Get rikishi information
pysumoapi rikishi 1511

# Get rikishi statistics
pysumoapi stats 1511

# Get shikona history for a rikishi
pysumoapi shikona --rikishi-id 1511

# Get measurements history for a rikishi
pysumoapi measurements --rikishi-id 1511

# Get rank history for a rikishi
pysumoapi ranks --rikishi-id 1511

# Get all shikona changes for a specific basho
pysumoapi shikona --basho-id 202305
```

## API Reference

### SumoClient

The main client class for interacting with the Sumo API.

```python
from pysumoapi.client import SumoClient

async with SumoClient() as client:
    # Use the client here
```

#### Methods

- `get_rikishi(rikishi_id: int) -> Rikishi`: Get information about a rikishi
- `get_rikishi_stats(rikishi_id: int) -> RikishiStats`: Get statistics for a rikishi
- `get_shikonas(rikishi_id: Optional[int] = None, basho_id: Optional[str] = None, sort_order: Optional[str] = "desc") -> List[Shikona]`: Get shikona history
- `get_measurements(rikishi_id: Optional[int] = None, basho_id: Optional[str] = None, sort_order: Optional[str] = "desc") -> List[Measurement]`: Get measurements history
- `get_ranks(rikishi_id: Optional[int] = None, basho_id: Optional[str] = None, sort_order: Optional[str] = "desc") -> List[Rank]`: Get rank history

### Data Models

- `Rikishi`: Information about a rikishi
- `RikishiStats`: Statistics for a rikishi
- `Shikona`: Shikona (ring name) information
- `Measurement`: Physical measurements of a rikishi
- `Rank`: Rank information for a rikishi

## Examples

See the [examples](examples/) directory for more detailed examples:

- [Shikona Example](examples/shikona_example.py): Demonstrates retrieving and displaying shikona history
- [Comprehensive Example](examples/comprehensive_example.py): Shows how to use multiple endpoints together to create a comprehensive rikishi profile

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/colebrumley/pysumoapi.git
cd pysumoapi

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### Using Make

This project includes a Makefile to automate common development tasks:

```bash
# Show available commands
make help

# Install the package in development mode
make install

# Install development dependencies
make dev

# Clean build artifacts and caches
make clean

# Run tests
make test

# Run linters
make lint

# Format code
make format

# Build the package
make build

# Publish to PyPI (requires PYPI_API_TOKEN environment variable)
make publish

# Build documentation (placeholder)
make docs

# Show current version
make version

# Bump version (major, minor, or patch)
make version-bump TYPE=patch

# Set version explicitly
make version-set VERSION=1.0.0
```

### Version Management

The package includes a version management script to help with versioning:

```bash
# Show current version
python scripts/version.py show

# Bump version (major, minor, or patch)
python scripts/version.py bump --type patch

# Set version explicitly
python scripts/version.py set --version 1.0.0
```

The script automatically updates both `pyproject.toml` and `CHANGELOG.md` when changing versions.

### Release Process

To create a new release:

1. Ensure you're on the `main` branch and it's up to date:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Run the release script:
   ```bash
   # For a patch release (0.1.0 -> 0.1.1)
   make release TYPE=patch

   # For a minor release (0.1.0 -> 0.2.0)
   make release TYPE=minor

   # For a major release (0.1.0 -> 1.0.0)
   make release TYPE=major
   ```

   The release script will:
   - Run pre-release checks
   - Bump the version
   - Run tests
   - Run linters
   - Build the package
   - Publish to PyPI (if PYPI_API_TOKEN is set)
   - Create a git tag

3. Follow the prompts to:
   - Commit the changes
   - Push to GitHub
   - Push the tag

You can skip certain steps using flags:
```bash
# Skip tests and linting
make release TYPE=patch --skip-tests --skip-lint

# Skip publishing to PyPI
make release TYPE=patch --skip-publish

# Skip creating a git tag
make release TYPE=patch --skip-tag

# Skip pre-release checks
make release TYPE=patch --skip-checks
```

## Security

Please see our [Security Policy](SECURITY.md) for information about:
- Supported versions
- How to report vulnerabilities
- Security best practices