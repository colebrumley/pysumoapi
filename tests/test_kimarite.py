import pytest
from datetime import datetime
from pysumoapi.client import SumoClient
from pysumoapi.models.kimarite import KimariteResponse


@pytest.mark.asyncio
async def test_get_kimarite_success():
    """Test successful retrieval of kimarite statistics."""
    async with SumoClient() as client:
        response = await client.get_kimarite(
            sort_field="count",
            sort_order="desc",
            limit=5
        )
        
        # Verify response type
        assert isinstance(response, KimariteResponse)
        
        # Verify query parameters are reflected
        assert response.sort_field == "count"
        assert response.sort_order == "desc"
        assert response.limit == 5
        assert response.skip == 0
        
        # Verify records
        assert len(response.records) == 5
        for record in response.records:
            assert record.count > 0
            # Verify last_usage format (YYYYMM-D or YYYYMM-DD)
            parts = record.last_usage.split("-")
            assert len(parts) == 2
            basho_date = parts[0]
            day = int(parts[1])
            assert len(basho_date) == 6
            assert 1 <= day <= 15
            
        # Verify sorting
        counts = [r.count for r in response.records]
        assert counts == sorted(counts, reverse=True)


@pytest.mark.asyncio
async def test_get_kimarite_invalid_sort_field():
    """Test handling of invalid sort field."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Invalid sort field"):
            await client.get_kimarite(sort_field="invalid")


@pytest.mark.asyncio
async def test_get_kimarite_invalid_sort_order():
    """Test handling of invalid sort order."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Sort order must be either 'asc' or 'desc'"):
            await client.get_kimarite(sort_order="invalid")


@pytest.mark.asyncio
async def test_get_kimarite_invalid_limit():
    """Test handling of invalid limit."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Limit must be a positive integer"):
            await client.get_kimarite(limit=-1)


@pytest.mark.asyncio
async def test_get_kimarite_invalid_skip():
    """Test handling of invalid skip."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Skip must be a non-negative integer"):
            await client.get_kimarite(skip=-1) 