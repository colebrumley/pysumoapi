# PySumoAPI Examples

This directory contains example scripts that demonstrate how to use the PySumoAPI library.

## Available Examples

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