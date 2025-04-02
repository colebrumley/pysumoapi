import asyncio
import httpx
from pysumoapi.client import SumoClient


async def main():
    """Test the ranks endpoint with real API data."""
    try:
        async with SumoClient() as client:
            # Get ranks for a specific basho
            print("\nRanks for Basho 196001:")
            ranks = await client.get_ranks(
                basho_id="196001",
                sort_order="desc"
            )
            
            print(f"\nFound {len(ranks)} ranks")
            print("-" * 50)
            
            for rank in ranks[:5]:  # Show first 5 records
                print(f"\nRikishi ID: {rank.rikishi_id}")
                print(f"Rank: {rank.rank}")
                print(f"Rank Value: {rank.rank_value}")
            
            # Get ranks for a specific rikishi
            print("\n\nRanks for Rikishi 1511:")
            ranks = await client.get_ranks(
                rikishi_id=1511,
                sort_order="asc"
            )
            
            print(f"\nFound {len(ranks)} ranks")
            print("-" * 50)
            
            for rank in ranks[:5]:  # Show first 5 records
                print(f"\nBasho: {rank.basho_id}")
                print(f"Rank: {rank.rank}")
                print(f"Rank Value: {rank.rank_value}")
    except httpx.HTTPStatusError as e:
        print(f"Error: {e}")
        print(f"Response: {e.response.text}")


if __name__ == "__main__":
    asyncio.run(main()) 