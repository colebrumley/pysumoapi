"""
Example demonstrating the HTTP configuration options in SumoClient.

This example shows how to configure timeouts, HTTP/2, and retry behavior.
"""

import asyncio
from pysumoapi import SumoClient


async def main():
    """Demonstrate different HTTP configuration options."""
    
    print("1. Using default configuration (5s timeouts, HTTP/2, 2 retries):")
    async with SumoClient() as client:
        try:
            rikishi = await client.get_rikishi("1")
            print(f"Found rikishi: {rikishi.shikona_en}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n2. Custom configuration with longer timeouts and more retries:")
    async with SumoClient(
        connect_timeout=10.0,
        read_timeout=15.0,
        max_retries=3,
        retry_backoff_factor=2.0,
        enable_http2=True,
    ) as client:
        try:
            rikishi = await client.get_rikishi("1")
            print(f"Found rikishi: {rikishi.shikona_en}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n3. Minimal configuration (HTTP/1.1, no retries):")
    async with SumoClient(
        connect_timeout=2.0,
        read_timeout=3.0,
        enable_http2=False,
        max_retries=0,
    ) as client:
        try:
            rikishi = await client.get_rikishi("1")
            print(f"Found rikishi: {rikishi.shikona_en}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
