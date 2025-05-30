# examples/sync_client_example.py

"""
Demonstrates the usage of the SumoSyncClient to interact with the Sumo API synchronously.
"""

from pysumoapi import SumoSyncClient
from pysumoapi.models import Rikishi, Basho  # Import relevant models for type hinting if desired

def main():
    """
    Main function to demonstrate SumoSyncClient usage.
    """
    print("Attempting to fetch data using SumoSyncClient...")

    # All constructor arguments from SumoClient are also available for SumoSyncClient
    # Ensure you use the client as a context manager
    with SumoSyncClient(base_url="https://sumo-api.com") as client:
        try:
            # Example 1: Get a specific rikishi
            print("\nFetching rikishi with ID 1 (Hakuhō)...")
            rikishi: Rikishi = client.get_rikishi(rikishi_id="1")
            if rikishi:
                print(f"Successfully fetched Rikishi: {rikishi.shikona_en}")
                print(f"  Heya: {rikishi.heya}")
                print(f"  Birthdate: {rikishi.birth_date}")
                if rikishi.shusshin:
                    print(f"  Shusshin (Origin): {rikishi.shusshin}")
            else:
                print("Rikishi not found or an error occurred.")

            # Example 2: Get details for a specific basho
            basho_id_to_fetch = "202307" # Nagoya Basho 2023
            print(f"\nFetching basho with ID {basho_id_to_fetch} (Nagoya 2023)...")
            basho: Basho = client.get_basho(basho_id=basho_id_to_fetch)
            if basho:
                print(f"Successfully fetched Basho: {basho.date}") # Use basho.date as the identifier
                print(f"  Location: {basho.location}")
                # The Basho model doesn't have a direct winner_id or schedule attribute.
                # Yusho information is in basho.yusho (a list of RikishiPrize)
                # For simplicity, let's print the Makuuchi yusho winner if available.
                makuuchi_yusho = next((y for y in basho.yusho if y.type == "Makuuchi"), None)
                if makuuchi_yusho:
                    print(f"  Makuuchi Yusho Winner: {makuuchi_yusho.shikona_en} (ID: {makuuchi_yusho.rikishi_id})")
                else:
                    print("  Makuuchi Yusho Winner: N/A")
                # Start and End dates are directly available
                print(f"  Start Date: {basho.start_date}")
                print(f"  End Date: {basho.end_date}")
            else:
                print(f"Basho {basho_id_to_fetch} not found or an error occurred.")

            # Example 3: Get a list of rikishi (with a small limit for brevity)
            print("\nFetching a list of active rikishi (limit 3)...")
            rikishi_list = client.get_rikishis(intai=False, limit=3) # Get active rikishi
            if rikishi_list and rikishi_list.records:
                print(f"Found {len(rikishi_list.records)} rikishi:")
                for r in rikishi_list.records:
                    print(f"  - {r.shikona_en} (ID: {r.id}, Heya: {r.heya})")
            else:
                print("No rikishi found or an error occurred.")

        except Exception as e:
            print(f"\nAn error occurred during API interaction: {e}")
            print("Please ensure the https://sumo-api.com is accessible and your query is valid.")

if __name__ == "__main__":
    main()
