import asyncio
from pysumoapi.client import SumoClient


async def main():
    """Test the kimarite matches endpoint with real API data."""
    async with SumoClient() as client:
        # Get recent matches where yorikiri was used
        response = await client.get_kimarite_matches(
            kimarite="yorikiri",
            sort_order="desc",
            limit=5
        )
        
        print(f"\nRecent {response.limit} Matches Using Yorikiri:")
        print(f"Total Matches Found: {response.total:,}")
        print("-" * 50)
        
        for match in response.records:
            print(f"\nBasho: {match.basho_id} - Day {match.day} - Match {match.match_no}")
            print(f"Division: {match.division}")
            print(f"East: {match.east_shikona} ({match.east_rank})")
            print(f"West: {match.west_shikona} ({match.west_rank})")
            print(f"Winner: {match.winner_en} ({match.winner_jp})")
            print(f"Kimarite: {match.kimarite}")


if __name__ == "__main__":
    asyncio.run(main()) 