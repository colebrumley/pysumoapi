"""Tests for the measurements endpoint."""

import pytest
from unittest.mock import patch

from pysumoapi.client import SumoClient
from pysumoapi.models import Measurement

# Test constants
TEST_RIKISHI_ID = 1511


@pytest.mark.asyncio
async def test_get_measurements_by_basho_success():
    """Test successful retrieval of measurements by basho."""
    mock_response = [
        {
            "id": "196001-1",
            "bashoId": "196001",
            "rikishiId": 1,
            "height": 180,
            "weight": 150,
        },
        {
            "id": "195911-1",
            "bashoId": "195911",
            "rikishiId": 1,
            "height": 180,
            "weight": 148,
        },
    ]

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            measurements = await client.get_measurements(
                basho_id="196001", sort_order="desc"
            )

        # Verify response type
        assert isinstance(measurements, list)
        assert all(isinstance(m, Measurement) for m in measurements)

        # Verify records
        assert len(measurements) > 0
        for measurement in measurements:
            assert measurement.rikishi_id > 0
            assert measurement.height > 0
            assert measurement.weight > 0
            assert measurement.id == f"{measurement.basho_id}-{measurement.rikishi_id}"

        # Verify sorting (by basho)
        basho_ids = [m.basho_id for m in measurements]
        assert basho_ids == sorted(basho_ids, reverse=True)


@pytest.mark.asyncio
async def test_get_measurements_by_rikishi_success():
    """Test successful retrieval of measurements by rikishi."""
    mock_response = [
        {
            "id": f"196001-{TEST_RIKISHI_ID}",
            "bashoId": "196001",
            "rikishiId": TEST_RIKISHI_ID,
            "height": 180,
            "weight": 150,
        },
        {
            "id": f"195911-{TEST_RIKISHI_ID}",
            "bashoId": "195911",
            "rikishiId": TEST_RIKISHI_ID,
            "height": 180,
            "weight": 148,
        },
    ]

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            measurements = await client.get_measurements(
                rikishi_id=TEST_RIKISHI_ID, sort_order="asc"
            )

        # Verify response type
        assert isinstance(measurements, list)
        assert all(isinstance(m, Measurement) for m in measurements)

        # Verify records
        assert len(measurements) > 0
        for measurement in measurements:
            assert measurement.rikishi_id == TEST_RIKISHI_ID
            assert measurement.height > 0
            assert measurement.weight > 0
            assert measurement.id == f"{measurement.basho_id}-{measurement.rikishi_id}"

        # Verify sorting (by basho)
        basho_ids = [m.basho_id for m in measurements]
        assert basho_ids == sorted(basho_ids)


@pytest.mark.asyncio
async def test_get_measurements_invalid_basho_id():
    """Test handling of invalid basho ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
            await client.get_measurements(basho_id="invalid")


@pytest.mark.asyncio
async def test_get_measurements_invalid_rikishi_id():
    """Test handling of invalid rikishi ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Rikishi ID must be positive"):
            await client.get_measurements(rikishi_id=-1)


@pytest.mark.asyncio
async def test_get_measurements_invalid_sort_order():
    """Test handling of invalid sort order."""
    async with SumoClient() as client:
        with pytest.raises(
            ValueError, match="Sort order must be either 'asc' or 'desc'"
        ):
            await client.get_measurements(basho_id="196001", sort_order="invalid")


@pytest.mark.asyncio
async def test_get_measurements_no_parameters():
    """Test handling of no parameters provided."""
    async with SumoClient() as client:
        with pytest.raises(
            ValueError, match="Either basho_id or rikishi_id must be provided"
        ):
            await client.get_measurements()
