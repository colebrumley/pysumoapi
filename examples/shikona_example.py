#!/usr/bin/env python3
"""
Example script demonstrating how to use the shikonas endpoint in PySumoAPI.

This script shows how to:
1. Get shikona changes for a specific rikishi
2. Get shikona changes for a specific basho
3. Sort shikona changes by basho ID
4. Display shikona history for a rikishi
"""

import asyncio
import sys
from typing import List, Optional
import httpx

from pysumoapi.client import SumoClient
from pysumoapi.models.shikonas import Shikona


async def get_rikishi_shikona_history(client: SumoClient, rikishi_id: int) -> list[Shikona]:
    """Get the shikona history for a specific rikishi."""
    return await client.get_shikonas(rikishi_id=rikishi_id, sort_order="asc")


async def get_basho_shikonas(client: SumoClient, basho_id: str) -> list[Shikona]:
    """Get all shikona changes for a specific basho."""
    return await client.get_shikonas(basho_id=basho_id, sort_order="asc")


def display_shikona_history(shikonas: List[Shikona], title: str) -> None:
    """
    Display shikona history in a formatted way.
    
    Args:
        shikonas: List of Shikona objects
        title: Title for the display
    """
    print(f"\n{title}")
    print("=" * 50)
    print(f"Found {len(shikonas)} shikona records")
    print("-" * 50)
    
    for shikona in shikonas:
        print(f"\nBasho: {shikona.basho_id}")
        print(f"Rikishi ID: {shikona.rikishi_id}")
        print(f"Shikona (EN): {shikona.shikona_en}")
        if shikona.shikona_jp:
            print(f"Shikona (JP): {shikona.shikona_jp}")
        print("-" * 30)


async def main():
    """Example usage of the shikona endpoint."""
    async with SumoClient() as client:
        try:
            # Get shikona history for a specific rikishi
            rikishi_id = 1511  # Example rikishi ID
            shikonas = await get_rikishi_shikona_history(client, rikishi_id)
            print(f"\nShikona history for Rikishi {rikishi_id}:")
            for shikona in shikonas:
                print(f"Basho: {shikona.basho_id}, Shikona: {shikona.shikona_en}")
                
            # Get all shikona changes for a specific basho
            basho_id = "202305"  # Example basho ID
            shikonas = await get_basho_shikonas(client, basho_id)
            print(f"\nShikona changes in Basho {basho_id}:")
            for shikona in shikonas:
                print(f"Rikishi: {shikona.rikishi_id}, Shikona: {shikona.shikona_en}")
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    sys.exit(asyncio.run(main())) 