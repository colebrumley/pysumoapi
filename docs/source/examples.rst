Examples
========

This page provides more detailed examples of using pysumoapi in various scenarios.

Tracking Tournament Progress
---------------------------

Here's how to track the progress of a tournament:

.. code-block:: python

    from pysumoapi import SumoClient
    from datetime import datetime

    client = SumoClient()
    
    # Get current basho
    basho = client.get_current_basho()
    print(f"Current basho: {basho.name}")
    
    # Get today's matches
    today = datetime.now().strftime("%Y-%m-%d")
    matches = client.get_matches(basho_id=basho.id, date=today)
    
    # Print match results
    for match in matches:
        print(f"{match.east.name} vs {match.west.name}: {match.result}")

Analyzing Rikishi Performance
----------------------------

Example of analyzing a rikishi's performance:

.. code-block:: python

    from pysumoapi import SumoClient
    from collections import Counter

    client = SumoClient()
    
    # Get rikishi information
    rikishi = client.get_rikishi("Terunofuji")
    
    # Get recent matches
    matches = client.get_matches(rikishi_id=rikishi.id, limit=100)
    
    # Analyze win/loss record
    results = Counter(match.result for match in matches)
    print(f"Win/Loss record: {results['win']}-{results['loss']}")
    
    # Calculate win percentage
    total_matches = sum(results.values())
    win_percentage = (results['win'] / total_matches) * 100
    print(f"Win percentage: {win_percentage:.1f}%")

Async Data Collection
-------------------

Example of collecting data asynchronously:

.. code-block:: python

    import asyncio
    from pysumoapi import AsyncSumoClient

    async def collect_rikishi_data():
        async with AsyncSumoClient() as client:
            # Get top division rikishi
            standings = await client.get_division_standings("Makuuchi")
            
            # Collect data for each rikishi
            tasks = [
                client.get_rikishi(rikishi.id)
                for rikishi in standings.rikishi
            ]
            
            # Gather all results
            rikishi_data = await asyncio.gather(*tasks)
            
            # Process the data
            for rikishi in rikishi_data:
                print(f"{rikishi.name}: {rikishi.rank}")

    asyncio.run(collect_rikishi_data())

CLI Scripting
------------

Example of using the CLI in a shell script:

.. code-block:: bash

    #!/bin/bash
    
    # Get current basho information
    BASHO_ID=$(pysumoapi basho current --json | jq -r '.id')
    
    # Get today's matches
    pysumoapi matches --basho "$BASHO_ID" --date "$(date +%Y-%m-%d)"
    
    # Get top division standings
    pysumoapi standings Makuuchi

Advanced Error Handling
---------------------

Example of comprehensive error handling:

.. code-block:: python

    from pysumoapi import SumoClient
    from pysumoapi.exceptions import (
        SumoAPIError,
        RikishiNotFoundError,
        BashoNotFoundError,
    )

    client = SumoClient()

    try:
        # Try to get rikishi data
        rikishi = client.get_rikishi("Terunofuji")
        
        # Try to get basho data
        basho = client.get_basho("202403")
        
        # Try to get matches
        matches = client.get_matches(
            basho_id=basho.id,
            rikishi_id=rikishi.id
        )
        
    except RikishiNotFoundError:
        print("Rikishi not found")
    except BashoNotFoundError:
        print("Basho not found")
    except SumoAPIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}") 