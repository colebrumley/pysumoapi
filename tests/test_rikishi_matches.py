"""Tests for the rikishi matches endpoint."""

from unittest.mock import AsyncMock, patch

import pytest

from pysumoapi.client import SumoClient
from pysumoapi.models import Match, RikishiMatchesResponse

# Test constants
TEST_LIMIT = 10
TEST_WEST_ID = 2


@pytest.mark.asyncio
async def test_get_rikishi_matches_success():
    """Test successful retrieval of rikishi matches."""
    rikishi_id = 1
    basho_id = "202401"

    mock_response = {
        "limit": TEST_LIMIT,
        "skip": 0,
        "total": 1,
        "records": [
            {
                "bashoId": basho_id,
                "division": "Makuuchi",
                "day": 1,
                "matchNo": 1,
                "eastId": 1,
                "eastShikona": "Test East",
                "eastRank": "M1",
                "westId": TEST_WEST_ID,
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
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ):
            response = await client.get_rikishi_matches(rikishi_id, basho_id)

    assert isinstance(response, RikishiMatchesResponse)
    assert response.limit == TEST_LIMIT
    assert response.skip == 0
    assert response.total == 1
    assert len(response.records) == 1

    first_match = response.records[0]
    assert isinstance(first_match, Match)
    assert first_match.basho_id == basho_id
    assert first_match.division == "Makuuchi"
    assert first_match.day == 1
    assert first_match.match_no == 1
    assert first_match.east_id == 1
    assert first_match.east_shikona == "Test East"
    assert first_match.east_rank == "M1"
    assert first_match.west_id == TEST_WEST_ID
    assert first_match.west_shikona == "Test West"
    assert first_match.west_rank == "M2"
    assert first_match.winner_id == 1
    assert first_match.winner_en == "Test East"
    assert first_match.winner_jp == "テスト東"
    assert first_match.kimarite == "yorikiri"


@pytest.mark.asyncio
async def test_get_rikishi_matches_invalid_rikishi():
    """Test error handling for invalid rikishi ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError):
            await client.get_rikishi_matches(-1)


@pytest.mark.asyncio
async def test_get_rikishi_matches_invalid_basho():
    """Test error handling for invalid basho ID format."""
    async with SumoClient() as client:
        with pytest.raises(ValueError):
            await client.get_rikishi_matches(1, basho_id="invalid")


@pytest.mark.asyncio
async def test_get_rikishi_matches_no_basho():
    """Test retrieval of all matches without basho filter."""
    mock_response = {
        "limit": TEST_LIMIT,
        "skip": 0,
        "total": 1,
        "records": [
            {
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
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ):
            response = await client.get_rikishi_matches(1)

    assert isinstance(response, RikishiMatchesResponse)
    assert response.limit == TEST_LIMIT
    assert response.skip == 0
    assert response.total == 1
    assert len(response.records) == 1

    first_match = response.records[0]
    assert isinstance(first_match, Match)
    assert first_match.basho_id == "202401"
    assert first_match.division == "Makuuchi"
    assert first_match.day == 1
    assert first_match.match_no == 1
    assert first_match.east_id == 1
    assert first_match.east_shikona == "Test East"
    assert first_match.east_rank == "M1"
    assert first_match.west_id == 2
    assert first_match.west_shikona == "Test West"
    assert first_match.west_rank == "M2"
    assert first_match.winner_id == 1
    assert first_match.winner_en == "Test East"
    assert first_match.winner_jp == "テスト東"
    assert first_match.kimarite == "yorikiri"
