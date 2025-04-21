from datetime import datetime
from typing import Any, Dict, Optional

import httpx
import ssl
from httpx import AsyncHTTPTransport
from httpx_retries import RetryTransport, Retry
from pydantic import BaseModel, Field

from pysumoapi.models import (
    Banzuke,
    Basho,
    KimariteMatchesResponse,
    KimariteResponse,
    Match,
    Measurement,
    MeasurementsResponse,
    Rank,
    RanksResponse,
    Rikishi,
    RikishiList,
    RikishiMatchesResponse,
    RikishiOpponentMatchesResponse,
    RikishiStats,
    Shikona,
    ShikonasResponse,
    Torikumi,
)


class SumoClient:
    """A client for interacting with the Sumo API."""

    def __init__(
        self,
        base_url: str = "https://sumo-api.com/api",
        timeout: Optional[float] = None,
        retries: int = 3,
    ) -> None:
        """Initialize the Sumo API client.

        Args:
            base_url: The base URL for the Sumo API
            timeout: The timeout for API requests in seconds, None for no timeout
            retries: The number of retries for failed requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "SumoClient":
        """Enter the async context manager."""
        retry = Retry(total=self.retries, backoff_factor=0.5)
        transport = RetryTransport(retry=retry)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            transport=transport,
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the async context manager."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Sumo API with retries.

        Args:
            method: The HTTP method to use
            path: The API path to request, with path parameters in {param_name} format
            params: Query parameters to include in the request, including path parameters
            json: JSON data to include in the request body

        Returns:
            The JSON response from the API

        Raises:
            httpx.HTTPError: If the request fails after all retries
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")

        # Extract path parameters from params and format the path
        path_params = {}
        if params:
            path_params = {k: v for k, v in params.items() if f"{{{k}}}" in path}
            query_params = {k: v for k, v in params.items() if f"{{{k}}}" not in path}
        else:
            query_params = {}

        # Format the path with path parameters
        formatted_path = path.format(**path_params)

        response = await self._client.request(
            method=method,
            url=formatted_path,
            params=query_params,
            json=json,
        )
        response.raise_for_status()
        return response.json()

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the Sumo API.

        Args:
            path: The API path to request
            params: Query parameters to include in the request

        Returns:
            The JSON response from the API
        """
        return await self._make_request("GET", path, params=params)

    async def post(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request to the Sumo API.

        Args:
            path: The API path to request
            json: JSON data to include in the request body

        Returns:
            The JSON response from the API
        """
        return await self._make_request("POST", path, json=json)

    async def put(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PUT request to the Sumo API.

        Args:
            path: The API path to request
            json: JSON data to include in the request body

        Returns:
            The JSON response from the API
        """
        return await self._make_request("PUT", path, json=json)

    async def delete(self, path: str) -> Dict[str, Any]:
        """Make a DELETE request to the Sumo API.

        Args:
            path: The API path to request

        Returns:
            The JSON response from the API
        """
        return await self._make_request("DELETE", path)

    async def get_rikishi(self, rikishi_id: str) -> Rikishi:
        """Get a single rikishi by ID."""
        data = await self.get("/rikishi/{rikishi_id}", params={"rikishi_id": rikishi_id})
        return Rikishi.model_validate(data)

    async def get_rikishi_stats(self, rikishi_id: str) -> RikishiStats:
        """Get statistics for a rikishi."""
        data = await self.get("/rikishi/{rikishi_id}/stats", params={"rikishi_id": rikishi_id})
        return RikishiStats.model_validate(data)

    async def get_rikishis(
        self,
        shikona_en: Optional[str] = None,
        heya: Optional[str] = None,
        sumodb_id: Optional[int] = None,
        nsk_id: Optional[int] = None,
        intai: Optional[bool] = None,
        measurements: bool = True,
        ranks: bool = True,
        shikonas: bool = True,
        limit: int = 10,
        skip: int = 0,
    ) -> RikishiList:
        """Get a list of rikishi with optional filters."""
        params = {
            "limit": limit,
            "skip": skip,
            "measurements": str(measurements).lower(),
            "ranks": str(ranks).lower(),
            "shikonas": str(shikonas).lower(),
        }

        if shikona_en:
            params["shikonaEn"] = shikona_en
        if heya:
            params["heya"] = heya
        if sumodb_id:
            params["sumodbId"] = sumodb_id
        if nsk_id:
            params["nskId"] = nsk_id
        if intai is not None:
            params["intai"] = str(intai).lower()

        data = await self.get("/rikishis", params=params)
        return RikishiList.model_validate(data)

    async def get_rikishi_matches(
        self, rikishi_id: int, basho_id: Optional[str] = None
    ) -> RikishiMatchesResponse:
        """
        Get all matches for a specific rikishi.

        Args:
            rikishi_id: The ID of the rikishi
            basho_id: Optional basho ID in YYYYMM format to filter matches

        Returns:
            RikishiMatchesResponse containing the matches

        Raises:
            ValueError: If rikishi_id is invalid or basho_id format is incorrect
        """
        if rikishi_id <= 0:
            raise ValueError("Rikishi ID must be positive")

        if basho_id and not (basho_id.isdigit() and len(basho_id) == 6):
            raise ValueError("Basho ID must be in YYYYMM format")

        params = {}
        if basho_id:
            params["bashoId"] = basho_id

        data = await self.get("/rikishi/{rikishi_id}/matches", params={"rikishi_id": rikishi_id, **params})
        
        # Convert matches to use the unified Match model
        if "records" in data:
            data["records"] = [
                Match.from_rikishi_match(match) for match in data["records"]
            ]
            
        return RikishiMatchesResponse.model_validate(data)

    async def get_rikishi_opponent_matches(
        self, rikishi_id: int, opponent_id: int, basho_id: Optional[str] = None
    ) -> RikishiOpponentMatchesResponse:
        """
        Get all matches between two specific rikishi.

        Args:
            rikishi_id: The ID of the first rikishi
            opponent_id: The ID of the second rikishi
            basho_id: Optional basho ID in YYYYMM format to filter matches

        Returns:
            RikishiOpponentMatchesResponse containing the matches between the two rikishi

        Raises:
            ValueError: If rikishi_id or opponent_id is invalid, or basho_id format is incorrect
        """
        if rikishi_id <= 0:
            raise ValueError("Rikishi ID must be positive")

        if opponent_id <= 0:
            raise ValueError("Opponent ID must be positive")

        if basho_id and not (basho_id.isdigit() and len(basho_id) == 6):
            raise ValueError("Basho ID must be in YYYYMM format")

        params = {}
        if basho_id:
            params["bashoId"] = basho_id

        data = await self.get("/rikishi/{rikishi_id}/matches/{opponent_id}", params={"rikishi_id": rikishi_id, "opponent_id": opponent_id, **params})
        return RikishiOpponentMatchesResponse.model_validate(data)

    async def get_basho(self, basho_id: str) -> Basho:
        """
        Get details for a specific basho tournament.

        Args:
            basho_id: The basho ID in YYYYMM format (e.g., 202305)

        Returns:
            Basho object containing tournament details, winners, and special prizes

        Raises:
            ValueError: If basho_id format is incorrect or date is in the future
        """
        if not (basho_id.isdigit() and len(basho_id) == 6):
            raise ValueError("Basho ID must be in YYYYMM format")

        # Check if date is in the future
        year = int(basho_id[:4])
        month = int(basho_id[4:])
        basho_date = datetime(year, month, 1)
        if basho_date > datetime.now():
            raise ValueError("Cannot get details for future basho")

        data = await self.get(f"/basho/{basho_id}")
        return Basho.model_validate(data)

    async def get_banzuke(self, basho_id: str, division: str) -> Banzuke:
        """Get banzuke details for a specific basho and division.

        Args:
            basho_id: Basho ID in YYYYMM format
            division: Division name (Makuuchi, Juryo, Makushita, Sandanme, Jonidan, Jonokuchi)

        Returns:
            Banzuke object containing the banzuke details

        Raises:
            ValueError: If basho_id is invalid or in the future, or if division is invalid
        """
        # Validate basho_id format
        try:
            year = int(basho_id[:4])
            month = int(basho_id[4:])
            basho_date = datetime(year, month, 1)
        except (ValueError, IndexError):
            raise ValueError("Basho ID must be in YYYYMM format")

        # Check if basho is in the future
        if basho_date > datetime.now():
            raise ValueError("Cannot fetch future basho")

        # Validate division
        valid_divisions = [
            "Makuuchi",
            "Juryo",
            "Makushita",
            "Sandanme",
            "Jonidan",
            "Jonokuchi",
        ]
        if division not in valid_divisions:
            raise ValueError("Invalid division")

        data = await self.get("/basho/{basho_id}/banzuke/{division}", params={"basho_id": basho_id, "division": division})

        # Process east and west sides
        for side in ["east", "west"]:
            if side in data:
                for rikishi in data[side]:
                    # Add side to each rikishi
                    rikishi["side"] = side.title()
                    # Convert record to Match objects
                    if "record" in rikishi:
                        # Add basho_id to each match record
                        for match in rikishi["record"]:
                            match["bashoId"] = basho_id
                        rikishi["record"] = [
                            Match.from_banzuke(match) for match in rikishi["record"]
                        ]

        # Ensure bashoId is set
        data["bashoId"] = basho_id

        return Banzuke.model_validate(data)

    async def get_torikumi(self, basho_id: str, division: str, day: int) -> Torikumi:
        """Get torikumi details for a specific basho, division, and day.

        Args:
            basho_id: Basho ID in YYYYMM format
            division: Division name (Makuuchi, Juryo, Makushita, Sandanme, Jonidan, Jonokuchi)
            day: Day of the tournament (1-15)

        Returns:
            Torikumi object containing the matches for the specified day

        Raises:
            ValueError: If basho_id is invalid or in the future, division is invalid, or day is out of range
        """
        # Validate basho_id format
        try:
            year = int(basho_id[:4])
            month = int(basho_id[4:])
            basho_date = datetime(year, month, 1)
        except (ValueError, IndexError):
            raise ValueError("Basho ID must be in YYYYMM format")

        # Check if basho is in the future
        if basho_date > datetime.now():
            raise ValueError("Cannot fetch future basho")

        # Validate division
        valid_divisions = [
            "Makuuchi",
            "Juryo",
            "Makushita",
            "Sandanme",
            "Jonidan",
            "Jonokuchi",
        ]
        if division not in valid_divisions:
            raise ValueError("Invalid division")

        # Validate day
        if not 1 <= day <= 15:
            raise ValueError("Day must be between 1 and 15")

        data = await self.get("/basho/{basho_id}/torikumi/{division}/{day}", params={"basho_id": basho_id, "division": division, "day": day})

        # Convert matches to use the unified Match model
        if "torikumi" in data:
            data["torikumi"] = [
                Match.from_torikumi(match) for match in data["torikumi"]
            ]
            
        # Handle both 'bashoId' and 'date' fields in the response
        if "bashoId" not in data and "date" in data:
            data["bashoId"] = data["date"]

        # Add division and day fields
        data["division"] = division
        data["day"] = day

        return Torikumi.model_validate(data)

    async def get_kimarite(
        self,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = None,
        skip: Optional[int] = 0,
    ) -> KimariteResponse:
        """Get statistics on kimarite usage.

        Args:
            sort_field: Field to sort by (count, kimarite, lastUsage)
            sort_order: Sort order (asc or desc)
            limit: Number of records to return
            skip: Number of records to skip

        Returns:
            KimariteResponse object containing kimarite statistics

        Raises:
            ValueError: If any of the parameters are invalid
        """
        # Validate parameters
        if sort_field and sort_field not in ["count", "kimarite", "lastUsage"]:
            raise ValueError(
                "Invalid sort field. Must be one of: count, kimarite, lastUsage"
            )

        if sort_order and sort_order not in ["asc", "desc"]:
            raise ValueError("Sort order must be either 'asc' or 'desc'")

        if limit is not None and limit <= 0:
            raise ValueError("Limit must be a positive integer")

        if skip < 0:
            raise ValueError("Skip must be a non-negative integer")

        # Build query parameters
        params: Dict[str, Any] = {}
        if sort_field:
            params["sortField"] = sort_field
        if sort_order:
            params["sortOrder"] = sort_order
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip

        data = await self.get("/kimarite", params=params)
        return KimariteResponse(**data)

    async def get_kimarite_matches(
        self,
        kimarite: str,
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = None,
        skip: Optional[int] = 0,
    ) -> KimariteMatchesResponse:
        """Get matches where a specific kimarite was used.

        Args:
            kimarite: Name of the kimarite to search for
            sort_order: Sort order (asc or desc)
            limit: Number of records to return (max 1000)
            skip: Number of records to skip

        Returns:
            KimariteMatchesResponse object containing matches

        Raises:
            ValueError: If any of the parameters are invalid
        """
        # Validate parameters
        if not kimarite:
            raise ValueError("Kimarite cannot be empty")

        if sort_order and sort_order not in ["asc", "desc"]:
            raise ValueError("Sort order must be either 'asc' or 'desc'")

        if limit is not None:
            if limit <= 0:
                raise ValueError("Limit must be a positive integer")
            if limit > 1000:
                raise ValueError("Limit cannot exceed 1000")

        if skip < 0:
            raise ValueError("Skip must be a non-negative integer")

        # Build query parameters
        params: Dict[str, Any] = {}
        if sort_order:
            params["sortOrder"] = sort_order
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip

        data = await self.get("/kimarite/{kimarite}", params={"kimarite": kimarite, **params})
        return KimariteMatchesResponse(**data)

    async def get_measurements(
        self,
        basho_id: Optional[str] = None,
        rikishi_id: Optional[int] = None,
        sort_order: Optional[str] = "desc",
    ) -> MeasurementsResponse:
        """Get measurement changes by rikishi or basho.

        Args:
            basho_id: Optional basho ID in YYYYMM format to filter measurements
            rikishi_id: Optional rikishi ID to filter measurements
            sort_order: Sort order for basho_id (asc or desc, default: desc)

        Returns:
            List[Measurement] containing measurement records

        Raises:
            ValueError: If parameters are invalid or neither basho_id nor rikishi_id is provided
        """
        # Validate parameters
        if not basho_id and not rikishi_id:
            raise ValueError("Either basho_id or rikishi_id must be provided")

        if basho_id and not (basho_id.isdigit() and len(basho_id) == 6):
            raise ValueError("Basho ID must be in YYYYMM format")

        if rikishi_id is not None and rikishi_id <= 0:
            raise ValueError("Rikishi ID must be positive")

        if sort_order and sort_order not in ["asc", "desc"]:
            raise ValueError("Sort order must be either 'asc' or 'desc'")

        # Build query parameters
        params: Dict[str, Any] = {}
        if basho_id:
            params["bashoId"] = basho_id
        if rikishi_id:
            params["rikishiId"] = rikishi_id

        data = await self.get("/measurements", params=params)
        # Convert each item in the list to a Measurement model
        measurements = [Measurement.model_validate(item) for item in data]

        # Sort by basho_id if requested
        if sort_order:
            measurements.sort(key=lambda m: m.basho_id, reverse=(sort_order == "desc"))

        return measurements

    async def get_ranks(
        self,
        basho_id: Optional[str] = None,
        rikishi_id: Optional[int] = None,
        sort_order: Optional[str] = "desc",
    ) -> RanksResponse:
        """Get rank changes by rikishi or basho.

        Args:
            basho_id: Optional basho ID in YYYYMM format to filter ranks
            rikishi_id: Optional rikishi ID to filter ranks
            sort_order: Sort order for basho_id (asc or desc, default: desc)

        Returns:
            List[Rank] containing rank records

        Raises:
            ValueError: If parameters are invalid or neither basho_id nor rikishi_id is provided
        """
        # Validate parameters
        if not basho_id and not rikishi_id:
            raise ValueError("Either basho_id or rikishi_id must be provided")

        if basho_id and not (basho_id.isdigit() and len(basho_id) == 6):
            raise ValueError("Basho ID must be in YYYYMM format")

        if rikishi_id is not None and rikishi_id <= 0:
            raise ValueError("Rikishi ID must be positive")

        if sort_order and sort_order not in ["asc", "desc"]:
            raise ValueError("Sort order must be either 'asc' or 'desc'")

        # Build query parameters
        params: Dict[str, Any] = {}
        if basho_id:
            params["bashoId"] = basho_id
        if rikishi_id:
            params["rikishiId"] = rikishi_id

        data = await self.get("/ranks", params=params)
        # Convert each item in the list to a Rank model
        ranks = [Rank.model_validate(item) for item in data]

        # Sort by basho_id if requested
        if sort_order:
            ranks.sort(key=lambda r: r.basho_id, reverse=(sort_order == "desc"))

        return ranks

    async def get_shikonas(
        self,
        basho_id: Optional[str] = None,
        rikishi_id: Optional[int] = None,
        sort_order: Optional[str] = "desc",
    ) -> ShikonasResponse:
        """Get shikona changes by rikishi or basho.

        Args:
            basho_id: Optional basho ID in YYYYMM format to filter shikonas
            rikishi_id: Optional rikishi ID to filter shikonas
            sort_order: Sort order for basho_id (asc or desc, default: desc)

        Returns:
            List[Shikona] containing shikona records

        Raises:
            ValueError: If parameters are invalid or neither basho_id nor rikishi_id is provided
        """
        # Validate parameters
        if not basho_id and not rikishi_id:
            raise ValueError("Either basho_id or rikishi_id must be provided")

        if basho_id and not (basho_id.isdigit() and len(basho_id) == 6):
            raise ValueError("Basho ID must be in YYYYMM format")

        if rikishi_id is not None and rikishi_id <= 0:
            raise ValueError("Rikishi ID must be positive")

        if sort_order and sort_order not in ["asc", "desc"]:
            raise ValueError("Sort order must be either 'asc' or 'desc'")

        # Build query parameters
        params: Dict[str, Any] = {}
        if basho_id:
            params["bashoId"] = basho_id
        if rikishi_id:
            params["rikishiId"] = rikishi_id

        data = await self.get("/shikonas", params=params)
        # Convert each item in the list to a Shikona model
        shikonas = [Shikona.model_validate(item) for item in data]

        # Sort by basho_id if requested
        if sort_order:
            shikonas.sort(key=lambda s: s.basho_id, reverse=(sort_order == "desc"))

        return shikonas
