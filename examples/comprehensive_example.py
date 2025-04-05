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
7. Look up kimarite statistics and matches
8. List rikishi with filters
9. Get matches between two rikishi
10. Get basho tournament details
11. Get banzuke details
12. Get torikumi (match schedule)
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


async def get_kimarite_analysis(client: SumoClient, kimarite: str = None) -> dict:
    """Get kimarite statistics and recent matches."""
    # Get general kimarite statistics
    kimarite_stats = await client.get_kimarite(
        sort_field="count", sort_order="desc", limit=10
    )

    # If a specific kimarite is provided, get recent matches using it
    kimarite_matches = None
    if kimarite:
        kimarite_matches = await client.get_kimarite_matches(
            kimarite=kimarite, sort_order="desc", limit=5
        )

    return {
        "stats": kimarite_stats,
        "matches": kimarite_matches,
    }


async def get_rikishi_matches_analysis(client: SumoClient, rikishi_id: int, opponent_id: int = None) -> dict:
    """Get matches for a rikishi and optionally against a specific opponent."""
    # Get all matches for the rikishi
    matches = await client.get_rikishi_matches(rikishi_id=rikishi_id)
    
    # If an opponent is specified, get matches between the two rikishi
    opponent_matches = None
    if opponent_id:
        opponent_matches = await client.get_rikishi_opponent_matches(
            rikishi_id=rikishi_id,
            opponent_id=opponent_id
        )
    
    return {
        "matches": matches,
        "opponent_matches": opponent_matches
    }


async def get_basho_details(client: SumoClient, basho_id: str) -> dict:
    """Get comprehensive details about a basho tournament."""
    try:
        # Get basic basho info
        basho = await client.get_basho(basho_id)
        
        # Get banzuke for Makuuchi division
        banzuke = await client.get_banzuke(basho_id=basho_id, division="Makuuchi")
        
        # Get torikumi for day 1
        torikumi = await client.get_torikumi(basho_id=basho_id, division="Makuuchi", day=1)
        
        return {
            "basho": basho,
            "banzuke": banzuke,
            "torikumi": torikumi
        }
    except Exception as e:
        print(f"Error in get_basho_details: {e}")
        import traceback
        traceback.print_exc()
        raise


async def search_rikishi(client: SumoClient, heya: str = None) -> dict:
    """Search for rikishi using various filters."""
    # Get list of rikishi from a specific heya
    rikishis = await client.get_rikishis(
        heya=heya,
        measurements=True,
        ranks=True,
        shikonas=True,
        limit=5
    )
    
    return {
        "rikishis": rikishis
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


def display_kimarite_analysis(analysis: Dict, kimarite: str = None) -> None:
    """Display kimarite statistics and matches."""
    print("\nKimarite Statistics (Top 10):")
    for stat in analysis["stats"].records:
        print(f"{stat.kimarite}: {stat.count} times")

    if kimarite and analysis["matches"]:
        print(f"\nRecent Matches using {kimarite}:")
        for match in analysis["matches"].records:
            print(f"Basho {match.basho_id} Day {match.day}: {match.east_shikona} vs {match.west_shikona} - Winner: {match.winner_en}")


def display_matches_analysis(analysis: Dict, opponent_id: int = None) -> None:
    """Display rikishi matches and opponent matches if available."""
    print("\nRecent Matches:")
    for match in analysis["matches"].records[:5]:  # Show last 5 matches
        print(f"Basho {match.basho_id} Day {match.day}: {match.east_shikona} vs {match.west_shikona} - Winner: {match.winner_en}")
    
    if opponent_id and analysis["opponent_matches"]:
        print(f"\nMatches against Rikishi {opponent_id}:")
        for match in analysis["opponent_matches"].matches:  # Changed from records to matches
            try:
                # Handle potential missing fields
                basho_id = getattr(match, "basho_id", "Unknown")
                day = getattr(match, "day", 0)
                east_shikona = getattr(match, "east_shikona", "Unknown")
                west_shikona = getattr(match, "west_shikona", "Unknown")
                winner_en = getattr(match, "winner_en", "Unknown")
                
                print(f"Basho {basho_id} Day {day}: {east_shikona} vs {west_shikona} - Winner: {winner_en}")
            except Exception as e:
                print(f"Error displaying match: {e}")
                # Print raw match data for debugging
                print(f"Match data: {match}")


def display_basho_details(analysis: Dict) -> None:
    """Display comprehensive basho tournament details."""
    basho = analysis["basho"]
    print(f"\nBasho Tournament: {basho.date}")
    print(f"Location: {basho.location}")
    print(f"Start Date: {basho.start_date}")
    print(f"End Date: {basho.end_date}")
    
    print("\nMakuuchi Banzuke:")
    print("East Side:")
    for rikishi in analysis["banzuke"].east:
        print(f"{rikishi.rank}: {rikishi.shikona_en}")
    print("\nWest Side:")
    for rikishi in analysis["banzuke"].west:
        print(f"{rikishi.rank}: {rikishi.shikona_en}")
    
    print("\nDay 1 Torikumi:")
    for match in analysis["torikumi"].matches:
        print(f"Match {match.match_no}: {match.east_shikona} vs {match.west_shikona}")


def display_rikishi_search(analysis: Dict) -> None:
    """Display results of rikishi search."""
    print("\nSearch Results:")
    for rikishi in analysis["rikishis"].records:
        print(f"\nRikishi ID: {rikishi.id}")
        print(f"Name: {rikishi.shikona_en}")
        print(f"Heya: {rikishi.heya}")
        # Rikishi model has direct height and weight fields, not a nested measurements object
        print(f"Height: {rikishi.height}cm")
        print(f"Weight: {rikishi.weight}kg")


async def main():
    """Example usage of multiple endpoints."""
    async with SumoClient() as client:
        try:
            # Example rikishi IDs
            rikishi_id = 1511  # Example rikishi ID
            opponent_id = 1512  # Example opponent ID
            basho_id = "202305"  # Example basho ID
            heya = "Miyagino"  # Example heya

            # Get career summary for a specific rikishi
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

            # Get and display kimarite analysis
            kimarite_analysis = await get_kimarite_analysis(client, "yorikiri")
            display_kimarite_analysis(kimarite_analysis, "yorikiri")

            # Get and display matches analysis
            matches_analysis = await get_rikishi_matches_analysis(client, rikishi_id, opponent_id)
            display_matches_analysis(matches_analysis, opponent_id)

            # Get and display basho details
            basho_details = await get_basho_details(client, basho_id)
            display_basho_details(basho_details)

            # Search for rikishi and display results
            rikishi_search = await search_rikishi(client, heya)
            display_rikishi_search(rikishi_search)

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {e!s}")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
