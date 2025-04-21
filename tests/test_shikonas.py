"""Tests for the shikonas endpoint."""

from unittest.mock import patch

import pytest

from pysumoapi.client import SumoClient
from pysumoapi.models import Shikona

# Test constants
TEST_RIKISHI_ID = 1511


@pytest.mark.asyncio
async def test_get_shikonas_by_basho_success():
    """Test successful retrieval of shikonas by basho."""
    mock_response = [
        {
            "id": "196001-1",
            "bashoId": "196001",
            "rikishiId": 1,
            "shikonaEn": "Test Shikona",
            "shikonaJp": "テスト四股名",
        }
    ]

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            shikonas = await client.get_shikonas(basho_id="196001", sort_order="desc")

            # Verify response type
            assert isinstance(shikonas, list)
            assert all(isinstance(s, Shikona) for s in shikonas)

            # Verify records
            assert len(shikonas) > 0
            for shikona in shikonas:
                assert shikona.rikishi_id > 0
                assert shikona.shikona_en
                assert shikona.id == f"{shikona.basho_id}-{shikona.rikishi_id}"

            # Verify sorting (by basho)
            basho_ids = [s.basho_id for s in shikonas]
            assert basho_ids == sorted(basho_ids, reverse=True)


@pytest.mark.asyncio
async def test_get_shikonas_by_rikishi_success():
    """Test successful retrieval of shikonas by rikishi."""
    mock_response = [
        {
            "id": "196001-1511",
            "bashoId": "196001",
            "rikishiId": TEST_RIKISHI_ID,
            "shikonaEn": "Test Shikona",
            "shikonaJp": "テスト四股名",
        }
    ]

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            shikonas = await client.get_shikonas(
                rikishi_id=TEST_RIKISHI_ID, sort_order="asc"
            )

            # Verify response type
            assert isinstance(shikonas, list)
            assert all(isinstance(s, Shikona) for s in shikonas)

            # Verify records
            assert len(shikonas) > 0
            for shikona in shikonas:
                assert shikona.rikishi_id == TEST_RIKISHI_ID
                assert shikona.shikona_en
                assert shikona.id == f"{shikona.basho_id}-{shikona.rikishi_id}"

            # Verify sorting (by basho)
            basho_ids = [s.basho_id for s in shikonas]
            assert basho_ids == sorted(basho_ids)


@pytest.mark.asyncio
async def test_get_shikonas_invalid_basho_id():
    """Test handling of invalid basho ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
            await client.get_shikonas(basho_id="invalid")


@pytest.mark.asyncio
async def test_get_shikonas_invalid_rikishi_id():
    """Test handling of invalid rikishi ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Rikishi ID must be positive"):
            await client.get_shikonas(rikishi_id=-1)


@pytest.mark.asyncio
async def test_get_shikonas_invalid_sort_order():
    """Test handling of invalid sort order."""
    async with SumoClient() as client:
        with pytest.raises(
            ValueError, match="Sort order must be either 'asc' or 'desc'"
        ):
            await client.get_shikonas(basho_id="196001", sort_order="invalid")


@pytest.mark.asyncio
async def test_get_shikonas_no_parameters():
    """Test handling of no parameters provided."""
    async with SumoClient() as client:
        with pytest.raises(
            ValueError, match="Either basho_id or rikishi_id must be provided"
        ):
            await client.get_shikonas()
