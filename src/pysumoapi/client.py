"""
Main client for interacting with the Sumo API.
"""
from typing import Optional, Dict, Any

import httpx
from pydantic import BaseModel

from .models import Rikishi, Basho, Kimarite, RikishiList, RikishiStats


class SumoAPI:
    """
    Client for interacting with the Sumo API.
    
    Args:
        base_url: The base URL of the API. Defaults to the official API URL.
        timeout: Timeout for API requests in seconds.
    """
    
    def __init__(
        self,
        base_url: str = "https://sumo-api.com/api",
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self) -> "SumoAPI":
        """Create and return the HTTP client when entering the context manager."""
        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close the HTTP client when exiting the context manager."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def get_rikishi(self, rikishi_id: str) -> Rikishi:
        """
        Get information about a specific rikishi.
        
        Args:
            rikishi_id: The ID of the rikishi to fetch.
            
        Returns:
            A Rikishi object containing the rikishi's information.
        """
        if not self._client:
            raise RuntimeError("Client must be used as an async context manager")
            
        url = f"{self.base_url}/rikishi/{rikishi_id}"
        response = await self._client.get(url)
        response.raise_for_status()
        return Rikishi.model_validate(response.json())

    async def get_rikishi_stats(self, rikishi_id: str) -> RikishiStats:
        """
        Get performance statistics for a specific rikishi.
        
        Args:
            rikishi_id: The ID of the rikishi to fetch stats for.
            
        Returns:
            A RikishiStats object containing the rikishi's performance statistics.
        """
        if not self._client:
            raise RuntimeError("Client must be used as an async context manager")
            
        url = f"{self.base_url}/rikishi/{rikishi_id}/stats"
        response = await self._client.get(url)
        response.raise_for_status()
        return RikishiStats.model_validate(response.json())

    async def get_rikishis(
        self,
        *,
        shikona_en: Optional[str] = None,
        heya: Optional[str] = None,
        sumodb_id: Optional[int] = None,
        nsk_id: Optional[int] = None,
        intai: Optional[bool] = None,
        measurements: bool = False,
        ranks: bool = False,
        shikonas: bool = False,
        limit: int = 100,
        skip: int = 0,
    ) -> RikishiList:
        """
        Get a list of rikishi matching the specified criteria.
        
        Args:
            shikona_en: Search for a rikishi by English shikona
            heya: Search by heya (stable), full name in English
            sumodb_id: Search by sumoDB ID
            nsk_id: Search by official NSK ID
            intai: If True, include retired rikishi. If None, only active rikishi.
            measurements: Include measurement history
            ranks: Include rank history
            shikonas: Include shikona history
            limit: How many results to return (max 1000)
            skip: Skip over the number of results specified
            
        Returns:
            A RikishiList object containing the paginated results.
        """
        if not self._client:
            raise RuntimeError("Client must be used as an async context manager")

        # Build query parameters
        params: Dict[str, Any] = {
            "limit": min(limit, 1000),  # Enforce API limit
            "skip": skip,
        }
        
        if shikona_en is not None:
            params["shikonaEn"] = shikona_en
        if heya is not None:
            params["heya"] = heya
        if sumodb_id is not None:
            params["sumodbId"] = sumodb_id
        if nsk_id is not None:
            params["nskId"] = nsk_id
        if intai is not None:
            params["intai"] = str(intai).lower()
        if measurements:
            params["measurements"] = "true"
        if ranks:
            params["ranks"] = "true"
        if shikonas:
            params["shikonas"] = "true"
            
        url = f"{self.base_url}/rikishis"
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return RikishiList.model_validate(response.json()) 