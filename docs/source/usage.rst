Usage Guide
===========

This guide will help you get started with pysumoapi. The library provides both synchronous and asynchronous clients for interacting with the Sumo API.

Basic Usage
-----------

First, import and create a client:

.. code-block:: python

    from pysumoapi import SumoClient

    # Create a synchronous client
    client = SumoClient()

    # Or create an async client
    from pysumoapi import AsyncSumoClient
    client = AsyncSumoClient()

Fetching Data
------------

The client provides methods to fetch various types of sumo data:

.. code-block:: python

    # Get current basho (tournament) information
    basho = client.get_current_basho()

    # Get rikishi (wrestler) information
    rikishi = client.get_rikishi("Terunofuji")

    # Get match results
    matches = client.get_matches(basho_id="202403")

    # Get division standings
    standings = client.get_division_standings("Makuuchi")

Async Usage
----------

When using the async client, make sure to use async/await:

.. code-block:: python

    import asyncio

    async def main():
        async with AsyncSumoClient() as client:
            basho = await client.get_current_basho()
            print(f"Current basho: {basho.name}")

    asyncio.run(main())

Error Handling
-------------

The library provides specific exceptions for different error cases:

.. code-block:: python

    from pysumoapi.exceptions import SumoAPIError

    try:
        rikishi = client.get_rikishi("NonExistentRikishi")
    except SumoAPIError as e:
        print(f"Error: {e}")

CLI Usage
---------

pysumoapi also provides a command-line interface:

.. code-block:: bash

    # Get current basho information
    pysumoapi basho current

    # Get rikishi information
    pysumoapi rikishi Terunofuji

    # Get match results
    pysumoapi matches --basho 202403

    # Get division standings
    pysumoapi standings Makuuchi

For more detailed examples, see the :doc:`examples` page. 