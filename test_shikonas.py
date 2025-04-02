import asyncio
import httpx
from pysumoapi.client import SumoClient


async def main():
    """Test the shikonas endpoint with real API data."""
    try:
        async with SumoClient() as client:
            # Get shikonas for a specific basho
            print("\nShikonas for Basho 196001:")
            shikonas = await client.get_shikonas(
                basho_id="196001",
                sort_order="desc"
            )
            
            print(f"\nFound {len(shikonas)} shikonas")
            print("-" * 50)
            
            for shikona in shikonas[:5]:  # Show first 5 records
                print(f"\nRikishi ID: {shikona.rikishi_id}")
                print(f"Shikona (EN): {shikona.shikona_en}")
                print(f"Shikona (JP): {shikona.shikona_jp}")
            
            # Get shikonas for a specific rikishi
            print("\n\nShikonas for Rikishi 1511:")
            shikonas = await client.get_shikonas(
                rikishi_id=1511,
                sort_order="asc"
            )
            
            print(f"\nFound {len(shikonas)} shikonas")
            print("-" * 50)
            
            for shikona in shikonas[:5]:  # Show first 5 records
                print(f"\nBasho: {shikona.basho_id}")
                print(f"Shikona (EN): {shikona.shikona_en}")
                print(f"Shikona (JP): {shikona.shikona_jp}")
    except httpx.HTTPStatusError as e:
        print(f"Error: {e}")
        print(f"Response: {e.response.text}")


if __name__ == "__main__":
    asyncio.run(main()) 