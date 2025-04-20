"""Tests for the ranks endpoint."""

import pytest
from unittest.mock import patch

from pysumoapi.client import SumoClient
from pysumoapi.models import Rank

# Test constants
TEST_RIKISHI_ID = 1511


@pytest.mark.asyncio
async def test_get_ranks_by_basho_success():
    """Test successful retrieval of ranks by basho."""
    mock_response = [
        {
            "id": "196001-1",
            "bashoId": "196001",
            "rikishiId": 1,
            "rank": "Y1e",
            "rankValue": 1,
        },
        {
            "id": "195911-1",
            "bashoId": "195911",
            "rikishiId": 1,
            "rank": "O1e",
            "rankValue": 2,
        },
    ]

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            ranks = await client.get_ranks(basho_id="196001", sort_order="desc")

        # Verify response type
        assert isinstance(ranks, list)
        assert all(isinstance(r, Rank) for r in ranks)

        # Verify records
        assert len(ranks) > 0
        for rank in ranks:
            assert rank.rikishi_id > 0
            assert rank.rank_value > 0
            assert rank.rank
            assert rank.id == f"{rank.basho_id}-{rank.rikishi_id}"

        # Verify sorting (by basho)
        basho_ids = [r.basho_id for r in ranks]
        assert basho_ids == sorted(basho_ids, reverse=True)


@pytest.mark.asyncio
async def test_get_ranks_by_rikishi_success():
    """Test successful retrieval of ranks by rikishi."""
    mock_response = [
        {
            "id": f"196001-{TEST_RIKISHI_ID}",
            "bashoId": "196001",
            "rikishiId": TEST_RIKISHI_ID,
            "rank": "M1e",
            "rankValue": 5,
        },
        {
            "id": f"195911-{TEST_RIKISHI_ID}",
            "bashoId": "195911",
            "rikishiId": TEST_RIKISHI_ID,
            "rank": "M2w",
            "rankValue": 6,
        },
    ]

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            ranks = await client.get_ranks(rikishi_id=TEST_RIKISHI_ID, sort_order="asc")

        # Verify response type
        assert isinstance(ranks, list)
        assert all(isinstance(r, Rank) for r in ranks)

        # Verify records
        assert len(ranks) > 0
        for rank in ranks:
            assert rank.rikishi_id == TEST_RIKISHI_ID
            assert rank.rank_value > 0
            assert rank.rank
            assert rank.id == f"{rank.basho_id}-{rank.rikishi_id}"

        # Verify sorting (by basho)
        basho_ids = [r.basho_id for r in ranks]
        assert basho_ids == sorted(basho_ids)


@pytest.mark.asyncio
async def test_get_ranks_invalid_basho_id():
    """Test handling of invalid basho ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
            await client.get_ranks(basho_id="invalid")


@pytest.mark.asyncio
async def test_get_ranks_invalid_rikishi_id():
    """Test handling of invalid rikishi ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Rikishi ID must be positive"):
            await client.get_ranks(rikishi_id=-1)


@pytest.mark.asyncio
async def test_get_ranks_invalid_sort_order():
    """Test handling of invalid sort order."""
    async with SumoClient() as client:
        with pytest.raises(
            ValueError, match="Sort order must be either 'asc' or 'desc'"
        ):
            await client.get_ranks(basho_id="196001", sort_order="invalid")


@pytest.mark.asyncio
async def test_get_ranks_no_parameters():
    """Test handling of no parameters provided."""
    async with SumoClient() as client:
        with pytest.raises(
            ValueError, match="Either basho_id or rikishi_id must be provided"
        ):
            await client.get_ranks()
