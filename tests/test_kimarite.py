"""Tests for the kimarite endpoint."""

import pytest
from unittest.mock import patch

from pysumoapi.client import SumoClient
from pysumoapi.models import KimariteResponse

# Test constants
TEST_LIMIT = 5
TEST_PARTS_COUNT = 2
TEST_BASHO_ID_LENGTH = 6
TEST_MAX_DAY = 15


@pytest.mark.asyncio
async def test_get_kimarite_success():
    """Test successful retrieval of kimarite statistics."""
    mock_response = {
        "sortField": "count",
        "sortOrder": "desc",
        "limit": TEST_LIMIT,
        "skip": 0,
        "total": TEST_LIMIT,
        "records": [
            {
                "kimarite": "yorikiri",
                "count": 100,
                "lastUsage": "202401-15",
            },
            {
                "kimarite": "oshidashi",
                "count": 90,
                "lastUsage": "202401-14",
            },
            {
                "kimarite": "hatakikomi",
                "count": 80,
                "lastUsage": "202401-13",
            },
            {
                "kimarite": "uwatenage",
                "count": 70,
                "lastUsage": "202401-12",
            },
            {
                "kimarite": "tsukidashi",
                "count": 60,
                "lastUsage": "202401-11",
            },
        ],
    }

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
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
    async with SumoClient() as client:
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
