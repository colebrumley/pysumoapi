"""Tests for the measurements endpoint."""

import pytest
from unittest.mock import patch

from pysumoapi.client import SumoClient
from pysumoapi.models import MeasurementsResponse
from pysumoapi.params import SortOrder

# Test constants
TEST_BASHO_ID = "202401"
TEST_RIKISHI_ID = 1
TEST_RECORDS_COUNT = 2


@pytest.mark.asyncio
async def test_get_measurements_success():
    """Test successful retrieval of measurements."""
    mock_response = [
        {
            "id": "202401-1",
            "bashoId": "202401",
            "rikishiId": 1,
            "height": 180,
            "weight": 150,
        },
        {
            "id": "202401-2",
            "bashoId": "202401",
            "rikishiId": 2,
            "height": 185,
            "weight": 160,
        },
    ]

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            response = await client.get_measurements(
                basho_id=TEST_BASHO_ID,
                rikishi_id=TEST_RIKISHI_ID,
                sort_order=SortOrder.desc
            )

        # Verify response type
        assert isinstance(response, list)
        assert len(response) == TEST_RECORDS_COUNT

        # Verify records
        for measurement in response:
            assert measurement.id.startswith(TEST_BASHO_ID)
            assert measurement.basho_id == TEST_BASHO_ID
            assert isinstance(measurement.rikishi_id, int)
            assert isinstance(measurement.height, float)
            assert isinstance(measurement.weight, float)

        # Verify sorting (by basho_id)
        basho_ids = [m.basho_id for m in response]
        assert basho_ids == sorted(basho_ids, reverse=True)


@pytest.mark.asyncio
async def test_get_measurements_invalid_basho_id():
    """Test handling of invalid basho ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
            await client.get_measurements("invalid", TEST_RIKISHI_ID)


@pytest.mark.asyncio
async def test_get_measurements_invalid_rikishi_id():
    """Test handling of invalid rikishi ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Rikishi ID must be positive"):
            await client.get_measurements(TEST_BASHO_ID, 0)


@pytest.mark.asyncio
async def test_get_measurements_invalid_sort_order():
    """Test handling of invalid sort order."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Sort order must be either 'asc' or 'desc'"):
            await client.get_measurements(
                TEST_BASHO_ID,
                TEST_RIKISHI_ID,
                "invalid"
            )
