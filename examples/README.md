# PySumoAPI Examples

This directory contains example scripts that demonstrate how to use the PySumoAPI library.
The library primarily features an asynchronous client (`SumoClient`) for efficient I/O operations.
It also offers a `SumoSyncClient` for synchronous operations, suitable for scripts or notebooks where async/await is not preferred. See the main [README.md](../README.md) for `SumoSyncClient` usage details.
The examples below primarily focus on the `SumoClient`, but a synchronous example is also provided.

## Available Examples

### `sync_client_example.py`

This example demonstrates how to use the `SumoSyncClient` for synchronous API calls. This is useful for scripts or interactive environments like Jupyter notebooks where `asyncio` might not be ideal. It shows how to:
- Instantiate `SumoSyncClient` as a context manager.
- Fetch data for a specific rikishi.
- Fetch details for a specific basho.
- Fetch a list of rikishi.

### `shikona_example.py`

This example demonstrates how to use the shikonas endpoint to:
- Get shikona changes for a specific rikishi
- Get shikona changes for a specific basho
- Sort shikona changes by basho ID
- Display shikona history for a rikishi

### `comprehensive_example.py`

This example demonstrates how to use multiple endpoints together to:
- Get rikishi information
- Get rikishi statistics
- Get rikishi matches
- Get rank changes
- Get shikona changes
- Analyze a rikishi's career progression

## Running the Examples

To run an example, use the following command:

```bash
python examples/shikona_example.py
# or
python examples/comprehensive_example.py
# or
python examples/sync_client_example.py
```

## Requirements

Make sure you have installed the PySumoAPI package:

```bash
pip install pysumoapi
```

## Notes

- The examples use real API data, so they require an internet connection.
- The examples use specific rikishi and basho IDs for demonstration purposes. You can modify these IDs to explore different data.
- The examples include error handling to gracefully handle API errors. 