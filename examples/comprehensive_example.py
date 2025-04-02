#!/usr/bin/env python3
"""
Comprehensive example demonstrating how to use multiple PySumoAPI endpoints together.

This script shows how to:
1. Get rikishi information
2. Get rikishi statistics
3. Get rikishi matches
4. Get rank changes
5. Get shikona changes
6. Analyze a rikishi's career progression
"""

import asyncio
import sys
from typing import Dict, List

import httpx

from pysumoapi.client import SumoClient
from pysumoapi.models.ranks import Rank
from pysumoapi.models.shikonas import Shikona


async def get_rikishi_career_summary(client: SumoClient, rikishi_id: int) -> dict:
    """Get a comprehensive career summary for a rikishi."""
    # Get basic rikishi info
    rikishi = await client.get_rikishi(rikishi_id)

    # Get rikishi stats
    stats = await client.get_rikishi_stats(rikishi_id)

    # Get shikona history
    shikonas = await client.get_shikonas(rikishi_id=rikishi_id, sort_order="asc")

    # Get measurements history
    measurements = await client.get_measurements(
        rikishi_id=rikishi_id, sort_order="asc"
    )

    # Get rank history
    ranks = await client.get_ranks(rikishi_id=rikishi_id, sort_order="asc")

    return {
        "rikishi": rikishi,
        "stats": stats,
        "shikonas": shikonas,
        "measurements": measurements,
        "ranks": ranks,
    }


def analyze_career_progression(ranks: List[Rank], shikonas: List[Shikona]) -> Dict:
    """
    Analyze a rikishi's career progression based on rank and shikona changes.

    Args:
        ranks: List of Rank objects
        shikonas: List of Shikona objects

    Returns:
        Dictionary containing career analysis
    """
    if not ranks:
        return {"error": "No rank data available"}

    # Get first and last rank
    first_rank = ranks[0]
    last_rank = ranks[-1]

    # Get first and last shikona
    first_shikona = shikonas[0] if shikonas else None
    last_shikona = shikonas[-1] if shikonas else None

    # Calculate career duration
    first_basho = first_rank.basho_id
    last_basho = last_rank.basho_id

    # Convert basho IDs to years (YYYYMM format)
    first_year = int(first_basho[:4])
    first_month = int(first_basho[4:])
    last_year = int(last_basho[:4])
    last_month = int(last_basho[4:])

    # Calculate years and months
    years = last_year - first_year
    months = last_month - first_month

    if months < 0:
        years -= 1
        months += 12

    # Format career duration
    if years > 0:
        duration = f"{years} year{'s' if years != 1 else ''}"
        if months > 0:
            duration += f" and {months} month{'s' if months != 1 else ''}"
    else:
        duration = f"{months} month{'s' if months != 1 else ''}"

    # Analyze rank progression
    rank_progression = []
    current_rank = None

    for rank in ranks:
        if rank.rank != current_rank:
            rank_progression.append({"basho": rank.basho_id, "rank": rank.rank})
            current_rank = rank.rank

    # Analyze shikona changes
    shikona_changes = []
    current_shikona = None

    for shikona in shikonas:
        if shikona.shikona_en != current_shikona:
            shikona_changes.append(
                {"basho": shikona.basho_id, "shikona": shikona.shikona_en}
            )
            current_shikona = shikona.shikona_en

    return {
        "first_basho": first_basho,
        "last_basho": last_basho,
        "career_duration": duration,
        "first_rank": first_rank.rank,
        "last_rank": last_rank.rank,
        "rank_progression": rank_progression,
        "shikona_changes": shikona_changes,
        "first_shikona": first_shikona.shikona_en if first_shikona else None,
        "current_shikona": last_shikona.shikona_en if last_shikona else None,
    }


def display_career_summary(rikishi_id: int, analysis: Dict) -> None:
    """
    Display a summary of a rikishi's career.

    Args:
        rikishi_id: The ID of the rikishi
        analysis: Dictionary containing career analysis
    """
    print(f"\nCareer Summary for Rikishi ID {rikishi_id}")
    print("=" * 50)

    if "error" in analysis:
        print(f"Error: {analysis['error']}")
        return

    print(f"Career Duration: {analysis['career_duration']}")
    print(f"First Basho: {analysis['first_basho']}")
    print(f"Last Basho: {analysis['last_basho']}")
    print(f"First Rank: {analysis['first_rank']}")
    print(f"Current Rank: {analysis['last_rank']}")

    if analysis["first_shikona"]:
        print(f"First Shikona: {analysis['first_shikona']}")
        print(f"Current Shikona: {analysis['current_shikona']}")

    print("\nRank Progression:")
    print("-" * 30)
    for rank_change in analysis["rank_progression"]:
        print(f"Basho {rank_change['basho']}: {rank_change['rank']}")

    if analysis["shikona_changes"]:
        print("\nShikona Changes:")
        print("-" * 30)
        for shikona_change in analysis["shikona_changes"]:
            print(f"Basho {shikona_change['basho']}: {shikona_change['shikona']}")


async def main():
    """Example usage of multiple endpoints."""
    async with SumoClient() as client:
        try:
            # Get career summary for a specific rikishi
            rikishi_id = 1511  # Example rikishi ID
            summary = await get_rikishi_career_summary(client, rikishi_id)

            # Print basic info
            rikishi = summary["rikishi"]
            print("\nRikishi Information:")
            print(f"Name: {rikishi.shikona_en}")
            print(f"Heya: {rikishi.heya}")
            print(f"Birth Date: {rikishi.birth_date.strftime('%Y-%m-%d')}")
            print(f"Height: {rikishi.height}cm")
            print(f"Weight: {rikishi.weight}kg")

            # Print career stats
            stats = summary["stats"]
            print("\nCareer Statistics:")
            print(f"Total Basho: {stats.basho}")
            print(f"Total Matches: {stats.total_matches}")
            print(f"Wins: {stats.total_wins}")
            print(f"Losses: {stats.total_losses}")
            print(f"Absences: {stats.total_absences}")
            print(f"Win Rate: {stats.total_wins / stats.total_matches:.2%}")
            print(f"Yusho: {stats.yusho}")

            # Print division stats
            print("\nDivision Statistics:")
            for division in ["Makuuchi", "Juryo", "Makushita", "Sandanme"]:
                if hasattr(stats.total_by_division, division):
                    print(f"\n{division}:")
                    print(
                        f"  Total Matches: {getattr(stats.total_by_division, division)}"
                    )
                    print(f"  Wins: {getattr(stats.wins_by_division, division)}")
                    print(f"  Losses: {getattr(stats.loss_by_division, division)}")
                    print(f"  Absences: {getattr(stats.absence_by_division, division)}")
                    print(f"  Yusho: {getattr(stats.yusho_by_division, division)}")

            # Print special prizes
            print("\nSpecial Prizes:")
            print(f"Gino-sho: {stats.sansho.Gino_sho}")
            print(f"Kanto-sho: {stats.sansho.Kanto_sho}")
            print(f"Shukun-sho: {stats.sansho.Shukun_sho}")

            # Print shikona history
            print("\nShikona History:")
            for shikona in summary["shikonas"]:
                print(f"Basho: {shikona.basho_id}, Shikona: {shikona.shikona_en}")

            # Print measurements history
            print("\nMeasurements History:")
            for measurement in summary["measurements"]:
                print(f"Basho: {measurement.basho_id}")
                print(f"  Height: {measurement.height}cm")
                print(f"  Weight: {measurement.weight}kg")

            # Print rank history
            print("\nRank History:")
            for rank in summary["ranks"]:
                print(f"Basho: {rank.basho_id}, Rank: {rank.rank}")

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {e!s}")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
