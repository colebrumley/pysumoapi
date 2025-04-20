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
from typing import Dict, List, Optional, Union

import httpx

from pysumoapi.client import SumoClient
from pysumoapi.models.ranks import Rank
from pysumoapi.models.shikonas import Shikona


async def get_rikishi_career_summary(client: SumoClient, rikishi_id: int) -> dict:
    """Get a comprehensive career summary for a rikishi."""
    try:
        # Get basic rikishi info
        rikishi = await client.get_rikishi(str(rikishi_id))

        # Get rikishi stats
        stats = await client.get_rikishi_stats(str(rikishi_id))

        # Get shikona history
        shikonas = await client.get_shikonas(rikishi_id=rikishi_id, sort_order="asc")

        # Get measurements history
        measurements = await client.get_measurements(
            rikishi_id=rikishi_id, sort_order="asc"
        )

        # Get rank history
        ranks = await client.get_ranks(rikishi_id=rikishi_id, sort_order="asc")

        # Process the career progression
        career_analysis = analyze_career_progression(ranks, shikonas)

        return {
            "rikishi": rikishi,
            "stats": stats,
            "shikonas": shikonas,
            "measurements": measurements,
            "ranks": ranks,
            "career_analysis": career_analysis
        }
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
        raise
    except Exception as e:
        print(f"An error occurred: {e!s}")
        raise


async def get_kimarite_analysis(client: SumoClient, kimarite: Optional[str] = None) -> dict:
    """Get kimarite statistics and recent matches."""
    try:
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
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
        raise
    except Exception as e:
        print(f"An error occurred: {e!s}")
        raise


async def get_rikishi_matches_analysis(
    client: SumoClient, 
    rikishi_identifier: Union[int, str], 
    opponent_identifier: Optional[Union[int, str]] = None
) -> dict:
    """
    Get matches for a rikishi and optionally against a specific opponent.
    
    Args:
        client: SumoClient instance
        rikishi_identifier: Either rikishi ID (int) or name (str)
        opponent_identifier: Optional opponent ID (int) or name (str)
        
    Returns:
        Dictionary containing matches data
    """
    try:
        # Get rikishi ID if name was provided
        rikishi_id = int(rikishi_identifier) if isinstance(rikishi_identifier, (int, str)) and str(rikishi_identifier).isdigit() else None
        if rikishi_id is None and isinstance(rikishi_identifier, str):
            rikishis = await client.get_rikishis(name=rikishi_identifier, limit=1)
            if not rikishis or not rikishis.records:
                raise ValueError(f"No rikishi found with name: {rikishi_identifier}")
            rikishi_id = int(rikishis.records[0].id)
            
        # Get opponent ID if name was provided
        opponent_id = int(opponent_identifier) if isinstance(opponent_identifier, (int, str)) and str(opponent_identifier).isdigit() else None
        if opponent_id is None and isinstance(opponent_identifier, str):
            opponents = await client.get_rikishis(name=opponent_identifier, limit=1)
            if not opponents or not opponents.records:
                raise ValueError(f"No opponent found with name: {opponent_identifier}")
            opponent_id = int(opponents.records[0].id)
        
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
            "rikishi_id": rikishi_id,
            "opponent_id": opponent_id,
            "matches": matches,
            "opponent_matches": opponent_matches
        }
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
        raise
    except Exception as e:
        print(f"An error occurred: {e!s}")
        raise


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
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
        raise
    except Exception as e:
        print(f"An error occurred: {e!s}")
        raise


async def search_rikishi(client: SumoClient, heya: Optional[str] = None) -> dict:
    """Search for rikishi using various filters."""
    try:
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
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
        raise
    except Exception as e:
        print(f"An error occurred: {e!s}")
        raise


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
    """Display kimarite statistics and matches in a formatted way."""
    print("\nKimarite Statistics (Top 10):")
    for stat in analysis["stats"].records:
        # Show all kimarite entries, including empty ones which are valid
        print(f"{stat.kimarite or '(no kimarite)'}: {stat.count} times")

    if kimarite and analysis["matches"]:
        print(f"\nRecent Matches using {kimarite}:")
        for match in analysis["matches"].records:
            if hasattr(match, 'east_shikona') and hasattr(match, 'west_shikona') and hasattr(match, 'winner_en'):
                print(f"Basho {match.basho_id} Day {match.day}: "
                      f"{match.east_shikona} vs {match.west_shikona} - "
                      f"Winner: {match.winner_en}")


async def display_rikishi_matches_analysis(
    client: SumoClient, 
    rikishi_identifier: Union[int, str], 
    opponent_identifier: Optional[Union[int, str]] = None
) -> None:
    """
    Display matches analysis for a rikishi and optionally against a specific opponent.
    
    Args:
        client: SumoClient instance
        rikishi_identifier: Either rikishi ID (int) or name (str)
        opponent_identifier: Optional opponent ID (int) or name (str)
    """
    print("\n=== Rikishi Matches Analysis ===")
    try:
        result = await get_rikishi_matches_analysis(
            client, 
            rikishi_identifier, 
            opponent_identifier
        )
        
        # Get rikishi name for display
        rikishi = await client.get_rikishi(str(result["rikishi_id"]))
        rikishi_name = rikishi.shikona_en if rikishi else f"Rikishi {result['rikishi_id']}"
        
        # Get opponent name if applicable
        opponent_name = None
        if result["opponent_id"]:
            opponent = await client.get_rikishi(str(result["opponent_id"]))
            opponent_name = opponent.shikona_en if opponent else f"Opponent {result['opponent_id']}"
        
        print(f"\nMatches for {rikishi_name}:")
        if result["matches"] and hasattr(result["matches"], "records"):
            for match in result["matches"].records[:5]:  # Show first 5 matches
                if hasattr(match, 'rikishi_shikona') and hasattr(match, 'opponent_shikona') and hasattr(match, 'kimarite'):
                    match_info = f"Basho {match.basho_id} Day {match.day}: "
                    match_info += f"{match.rikishi_shikona} vs {match.opponent_shikona} "
                    match_info += f"({match.kimarite or '(no kimarite)'})"
                    print(f"- {match_info}")
            
        if opponent_name and result["opponent_matches"] and hasattr(result["opponent_matches"], "records"):
            print(f"\nMatches specifically against {opponent_name}:")
            for match in result["opponent_matches"].records[:5]:  # Show first 5 matches
                if hasattr(match, 'kimarite'):
                    match_info = f"Basho {match.basho_id} Day {match.day}"
                    match_info += f": {match.kimarite or '(no kimarite)'}"
                    print(f"- {match_info}")
                
    except Exception as e:
        print(f"Error displaying matches analysis: {e!s}")
        raise


def display_basho_details(analysis: Dict) -> None:
    """Display comprehensive basho details."""
    basho = analysis["basho"]
    banzuke = analysis["banzuke"]
    torikumi = analysis["torikumi"]

    print("\nBasho Details:")
    print("=" * 50 + "\n")
    print(f"Basho {basho.date}:")
    print("-" * 30)
    print(f"Location: {basho.location}")
    print(f"Start Date: {basho.start_date}")
    print(f"End Date: {basho.end_date}\n")

    print("Banzuke (Makuuchi):")
    print("-" * 30)
    # Show top 5 ranks from east and west sides
    for i in range(min(5, len(banzuke.east))):
        east = banzuke.east[i]
        west = banzuke.west[i] if i < len(banzuke.west) else None
        if west:
            print(f"{east.rank}: {east.shikona_en} / {west.shikona_en}")
        else:
            print(f"{east.rank}: {east.shikona_en}")

    print("\nDay 1 Torikumi (Makuuchi):")
    print("-" * 30)
    if torikumi and torikumi.matches:
        for match in torikumi.matches[:5]:  # Show first 5 matches
            print(f"{match.east_shikona} vs {match.west_shikona}")
            if match.winner_en:
                print(f"Winner: {match.winner_en}")
            if match.kimarite:
                print(f"Technique: {match.kimarite}")
            print()
    else:
        print("No matches available for Day 1")


def display_rikishi_search(analysis: Dict) -> None:
    """Display rikishi search results in a formatted way."""
    print("\nRikishi Search Results:")
    print("=" * 50)

    if analysis["rikishis"]:
        for rikishi in analysis["rikishis"].records:
            print(f"\nRikishi ID: {rikishi.id}")
            print("-" * 30)
            print(f"Name: {rikishi.shikona_en}")
            print(f"Heya: {rikishi.heya}")
            if rikishi.current_rank:
                print(f"Current Rank: {rikishi.current_rank}")
            print("-" * 30)


async def main():
    """Run comprehensive examples of PySumoAPI usage."""
    # Initialize client with retry configuration and correct base URL
    client = SumoClient(
        base_url="https://sumo-api.com/api",
        retries=3,
        timeout=30.0
    )
    
    async with client:
        try:
            # Example 1: Get career summary for a rikishi
            rikishi_id = 1511  # Terunofuji
            career_summary = await get_rikishi_career_summary(client, rikishi_id)
            display_career_summary(rikishi_id, career_summary["career_analysis"])

            # Example 2: Analyze kimarite usage
            kimarite_analysis = await get_kimarite_analysis(client, "yoritaoshi")
            display_kimarite_analysis(kimarite_analysis, "yoritaoshi")

            # Example 3: Get matches analysis
            await display_rikishi_matches_analysis(client, rikishi_id)

            # Example 4: Get basho details
            basho_id = "202401"  # January 2024 basho
            basho_details = await get_basho_details(client, basho_id)
            display_basho_details(basho_details)

            # Example 5: Search for rikishi
            search_results = await search_rikishi(client, heya="Isegahama")
            display_rikishi_search(search_results)

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e!s}")
            sys.exit(1)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
