"""Tests for the kimarite matches endpoint."""

import pytest
from unittest.mock import patch

from pysumoapi.client import SumoClient
from pysumoapi.models import KimariteMatchesResponse
from pysumoapi.params import Pagination, SortOrder

# Test constants
TEST_LIMIT = 5
TEST_RECORDS_COUNT = 2
TEST_MAX_DAY = 15


@pytest.mark.asyncio
async def test_get_kimarite_matches_success():
    """Test successful retrieval of kimarite matches."""
    mock_response = {
        "limit": TEST_LIMIT,
        "skip": 0,
        "total": TEST_RECORDS_COUNT,
        "records": [
            {
                "id": "202401-2-1",
                "bashoId": "202401",
                "division": "Makuuchi",
                "day": 2,
                "matchNo": 1,
                "eastId": 1,
                "eastShikona": "Test East",
                "eastRank": "M1",
                "westId": 2,
                "westShikona": "Test West",
                "westRank": "M2",
                "winnerId": 1,
                "winnerEn": "Test East",
                "winnerJp": "テスト東",
                "kimarite": "yorikiri",
            },
            {
                "id": "202401-1-1",
                "bashoId": "202401",
                "division": "Makuuchi",
                "day": 1,
                "matchNo": 1,
                "eastId": 1,
                "eastShikona": "Test East",
                "eastRank": "M1",
                "westId": 2,
                "westShikona": "Test West",
                "westRank": "M2",
                "winnerId": 1,
                "winnerEn": "Test East",
                "winnerJp": "テスト東",
                "kimarite": "yorikiri",
            },
        ],
    }

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            response = await client.get_kimarite_matches(
                kimarite="yorikiri",
                sort_order=SortOrder.desc,
                pagination=Pagination(limit=TEST_LIMIT)
            )

        # Verify response type
        assert isinstance(response, KimariteMatchesResponse)

        # Verify query parameters are reflected
        assert response.limit == TEST_LIMIT
        assert response.skip == 0
        assert response.total > 0

        # Verify records
        assert len(response.records) == TEST_RECORDS_COUNT
        for match in response.records:
            assert match.kimarite == "yorikiri"
            assert match.id.startswith("202401")
            assert match.basho_id == "202401"
            assert match.division == "Makuuchi"
            assert 1 <= match.day <= TEST_MAX_DAY
            assert match.match_no > 0
            assert isinstance(match.east_id, int)
            assert match.east_shikona == "Test East"
            assert match.east_rank == "M1"
            assert isinstance(match.west_id, int)
            assert match.west_shikona == "Test West"
            assert match.west_rank == "M2"
            assert isinstance(match.winner_id, int)
            assert match.winner_en == "Test East"
            assert match.winner_jp == "テスト東"

        # Verify sorting (by basho and day)
        basho_days = [(m.basho_id, m.day) for m in response.records]
        assert basho_days == sorted(basho_days, reverse=True)


@pytest.mark.asyncio
async def test_get_kimarite_matches_empty_kimarite():
    """Test handling of empty kimarite."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Kimarite cannot be empty"):
            await client.get_kimarite_matches("")


@pytest.mark.asyncio
async def test_get_kimarite_matches_skip_zero():
    """Test that skip=0 is properly handled."""
    mock_response = {
        "limit": TEST_LIMIT,
        "skip": 0,
        "total": 1,
        "records": [
            {
                "id": "202401-1-1",
                "bashoId": "202401",
                "division": "Makuuchi",
                "day": 1,
                "matchNo": 1,
                "eastId": 1,
                "eastShikona": "Test East",
                "eastRank": "M1",
                "westId": 2,
                "westShikona": "Test West",
                "westRank": "M2",
                "winnerId": 1,
                "winnerEn": "Test East",
                "winnerJp": "テスト東",
                "kimarite": "yorikiri",
            }
        ],
    }

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            response = await client.get_kimarite_matches(
                "yorikiri",
                sort_order=SortOrder.desc,
                pagination=Pagination(limit=TEST_LIMIT, skip=0)
            )

        # Verify response type
        assert isinstance(response, KimariteMatchesResponse)

        # Verify query parameters are reflected
        assert response.limit == TEST_LIMIT
        assert response.skip == 0
        assert response.total == 1

        # Verify records
        assert len(response.records) == 1
        match = response.records[0]
        assert match.id == "202401-1-1"
        assert match.basho_id == "202401"
        assert match.division == "Makuuchi"
        assert match.day == 1
        assert match.match_no == 1
        assert match.east_id == 1
        assert match.east_shikona == "Test East"
        assert match.east_rank == "M1"
        assert match.west_id == 2
        assert match.west_shikona == "Test West"
        assert match.west_rank == "M2"
        assert match.winner_id == 1
        assert match.winner_en == "Test East"
        assert match.winner_jp == "テスト東"
        assert match.kimarite == "yorikiri"
