import asyncio
import httpx
from pysumoapi.client import SumoClient


async def main():
    """Test the measurements endpoint with real API data."""
    try:
        async with SumoClient() as client:
            # Get measurements for a specific basho
            print("\nMeasurements for Basho 196001:")
            measurements = await client.get_measurements(
                basho_id="196001",
                sort_order="desc"
            )
            
            print(f"\nFound {len(measurements)} measurements")
            print("-" * 50)
            
            for measurement in measurements[:5]:  # Show first 5 records
                print(f"\nRikishi ID: {measurement.rikishi_id}")
                print(f"Height: {measurement.height}cm")
                print(f"Weight: {measurement.weight}kg")
            
            # Get measurements for a specific rikishi
            print("\n\nMeasurements for Rikishi 1511:")
            measurements = await client.get_measurements(
                rikishi_id=1511,
                sort_order="asc"
            )
            
            print(f"\nFound {len(measurements)} measurements")
            print("-" * 50)
            
            for measurement in measurements[:5]:  # Show first 5 records
                print(f"\nBasho: {measurement.basho_id}")
                print(f"Height: {measurement.height}cm")
                print(f"Weight: {measurement.weight}kg")
    except httpx.HTTPStatusError as e:
        print(f"Error: {e}")
        print(f"Response: {e.response.text}")


if __name__ == "__main__":
    asyncio.run(main()) 