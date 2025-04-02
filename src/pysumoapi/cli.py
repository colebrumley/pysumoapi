#!/usr/bin/env python3
"""
Command-line interface for PySumoAPI.
"""

import argparse
import asyncio
import json
import sys
from typing import Optional

from pysumoapi.client import SumoClient


async def get_rikishi_info(client: SumoClient, rikishi_id: int) -> None:
    """Get and display information about a rikishi."""
    try:
        rikishi = await client.get_rikishi(rikishi_id)
        print(json.dumps(rikishi.model_dump(), indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def get_rikishi_stats(client: SumoClient, rikishi_id: int) -> None:
    """Get and display statistics for a rikishi."""
    try:
        stats = await client.get_rikishi_stats(rikishi_id)
        print(json.dumps(stats.model_dump(), indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def get_shikona_history(client: SumoClient, rikishi_id: Optional[int] = None, basho_id: Optional[str] = None) -> None:
    """Get and display shikona history."""
    try:
        shikonas = await client.get_shikonas(rikishi_id=rikishi_id, basho_id=basho_id, sort_order="asc")
        print(json.dumps([s.model_dump() for s in shikonas], indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def get_measurements(client: SumoClient, rikishi_id: Optional[int] = None, basho_id: Optional[str] = None) -> None:
    """Get and display measurements history."""
    try:
        measurements = await client.get_measurements(rikishi_id=rikishi_id, basho_id=basho_id, sort_order="asc")
        print(json.dumps([m.model_dump() for m in measurements], indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def get_ranks(client: SumoClient, rikishi_id: Optional[int] = None, basho_id: Optional[str] = None) -> None:
    """Get and display rank history."""
    try:
        ranks = await client.get_ranks(rikishi_id=rikishi_id, basho_id=basho_id, sort_order="asc")
        print(json.dumps([r.model_dump() for r in ranks], indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="PySumoAPI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Rikishi info command
    rikishi_parser = subparsers.add_parser("rikishi", help="Get rikishi information")
    rikishi_parser.add_argument("rikishi_id", type=int, help="Rikishi ID")
    
    # Rikishi stats command
    stats_parser = subparsers.add_parser("stats", help="Get rikishi statistics")
    stats_parser.add_argument("rikishi_id", type=int, help="Rikishi ID")
    
    # Shikona history command
    shikona_parser = subparsers.add_parser("shikona", help="Get shikona history")
    shikona_parser.add_argument("--rikishi-id", type=int, help="Rikishi ID")
    shikona_parser.add_argument("--basho-id", help="Basho ID (YYYYMM format)")
    
    # Measurements command
    measurements_parser = subparsers.add_parser("measurements", help="Get measurements history")
    measurements_parser.add_argument("--rikishi-id", type=int, help="Rikishi ID")
    measurements_parser.add_argument("--basho-id", help="Basho ID (YYYYMM format)")
    
    # Ranks command
    ranks_parser = subparsers.add_parser("ranks", help="Get rank history")
    ranks_parser.add_argument("--rikishi-id", type=int, help="Rikishi ID")
    ranks_parser.add_argument("--basho-id", help="Basho ID (YYYYMM format)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    async def run_command() -> None:
        async with SumoClient() as client:
            if args.command == "rikishi":
                await get_rikishi_info(client, args.rikishi_id)
            elif args.command == "stats":
                await get_rikishi_stats(client, args.rikishi_id)
            elif args.command == "shikona":
                await get_shikona_history(client, args.rikishi_id, args.basho_id)
            elif args.command == "measurements":
                await get_measurements(client, args.rikishi_id, args.basho_id)
            elif args.command == "ranks":
                await get_ranks(client, args.rikishi_id, args.basho_id)
    
    asyncio.run(run_command())


if __name__ == "__main__":
    main() 