"""Tests for the kimarite endpoint."""

import pytest

from pysumoapi.client import SumoClient
from pysumoapi.models import KimariteResponse

# Test constants
TEST_LIMIT = 5
TEST_PARTS_COUNT = 2
TEST_BASHO_ID_LENGTH = 6
TEST_MAX_DAY = 20  # Allow for potential playoff/extra days beyond standard 15


@pytest.mark.asyncio
async def test_get_kimarite_success():
    """Test successful retrieval of kimarite statistics."""
    async with SumoClient() as client:
        response = await client.get_kimarite(
            sort_field="count", sort_order="desc", limit=TEST_LIMIT
        )

        # Verify response type
        assert isinstance(response, KimariteResponse)

        # Verify query parameters are reflected
        assert response.sort_field == "count"
        assert response.sort_order == "desc"
        assert response.limit == TEST_LIMIT
        assert response.skip == 0

        # Verify records
        assert len(response.records) == TEST_LIMIT
        for record in response.records:
            assert record.count > 0
            # Verify last_usage format (YYYYMM-D or YYYYMM-DD)
            parts = record.last_usage.split("-")
            assert len(parts) == TEST_PARTS_COUNT
            basho_date = parts[0]
            day = int(parts[1])
            assert len(basho_date) == TEST_BASHO_ID_LENGTH
            assert 1 <= day <= TEST_MAX_DAY

        # Verify sorting
        counts = [r.count for r in response.records]
        assert counts == sorted(counts, reverse=True)


@pytest.mark.asyncio
async def test_get_kimarite_invalid_sort_field():
    """Test handling of invalid sort field."""
    async with SumoClient(verify_ssl=False) as client:
        with pytest.raises(ValueError):
            await client.get_kimarite(sort_field="invalid_field")


@pytest.mark.asyncio
async def test_get_kimarite_invalid_sort_order():
    """Test handling of invalid sort order."""
    async with SumoClient() as client:
        with pytest.raises(
            ValueError, match="Sort order must be either 'asc' or 'desc'"
        ):
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
