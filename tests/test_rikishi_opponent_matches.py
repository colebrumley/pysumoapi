"""Tests for the rikishi opponent matches endpoint."""

from unittest.mock import AsyncMock, patch

import pytest

from pysumoapi.client import SumoClient
from pysumoapi.models import Match, RikishiOpponentMatchesResponse

# Test constants
TEST_TOTAL_MATCHES = 13
TEST_RIKISHI_WINS = 5
TEST_OPPONENT_WINS = 8
TEST_DAY = 15
TEST_MATCH_NO = 19
TEST_WEST_ID = 45
TEST_WINNER_ID = 45


@pytest.mark.asyncio
async def test_get_rikishi_opponent_matches_success():
    """Test successful retrieval of matches between two rikishi."""
    rikishi_id = 1
    opponent_id = 45
    basho_id = "202401"

    mock_response = {
        "matches": [
            {
                "bashoId": basho_id,
                "division": "Makuuchi",
                "day": 15,
                "matchNo": 19,
                "eastId": 1,
                "eastShikona": "Takakeisho",
                "eastRank": "Ozeki 1 East",
                "westId": 45,
                "westShikona": "Terunofuji",
                "westRank": "Komusubi 1 East",
                "kimarite": "abisetaoshi",
                "winnerId": 45,
                "winnerEn": "Terunofuji",
                "winnerJp": "",
            }
        ],
        "kimariteLosses": {"abisetaoshi": 1, "hatakikomi": 2},
        "kimariteWins": {"oshidashi": 4, "tsukiotoshi": 1},
        "opponentWins": 8,
        "rikishiWins": 5,
        "total": 13,
    }

    async with SumoClient() as client:
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ):
            response = await client.get_rikishi_opponent_matches(
                rikishi_id, opponent_id, basho_id
            )

    assert isinstance(response, RikishiOpponentMatchesResponse)
    assert response.total == TEST_TOTAL_MATCHES
    assert response.rikishi_wins == TEST_RIKISHI_WINS
    assert response.opponent_wins == TEST_OPPONENT_WINS
    assert len(response.matches) == 1
    assert response.kimarite_wins == {"oshidashi": 4, "tsukiotoshi": 1}
    assert response.kimarite_losses == {"abisetaoshi": 1, "hatakikomi": 2}

    first_match = response.matches[0]
    assert isinstance(first_match, Match)
    assert first_match.basho_id == basho_id
    assert first_match.division == "Makuuchi"
    assert first_match.day == TEST_DAY
    assert first_match.match_no == TEST_MATCH_NO
    assert first_match.east_id == 1
    assert first_match.east_shikona == "Takakeisho"
    assert first_match.east_rank == "Ozeki 1 East"
    assert first_match.west_id == TEST_WEST_ID
    assert first_match.west_shikona == "Terunofuji"
    assert first_match.west_rank == "Komusubi 1 East"
    assert first_match.kimarite == "abisetaoshi"
    assert first_match.winner_id == TEST_WINNER_ID
    assert first_match.winner_en == "Terunofuji"
    assert first_match.winner_jp == ""


@pytest.mark.asyncio
async def test_get_rikishi_opponent_matches_invalid_rikishi():
    """Test error handling for invalid rikishi ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError):
            await client.get_rikishi_opponent_matches(-1, 45)


@pytest.mark.asyncio
async def test_get_rikishi_opponent_matches_invalid_opponent():
    """Test error handling for invalid opponent ID."""
    async with SumoClient() as client:
        with pytest.raises(ValueError):
            await client.get_rikishi_opponent_matches(1, -1)


@pytest.mark.asyncio
async def test_get_rikishi_opponent_matches_invalid_basho():
    """Test error handling for invalid basho ID format."""
    async with SumoClient() as client:
        with pytest.raises(ValueError):
            await client.get_rikishi_opponent_matches(1, 45, basho_id="invalid")


@pytest.mark.asyncio
async def test_get_rikishi_opponent_matches_no_basho():
    """Test retrieval of all matches without basho filter."""
    mock_response = {
        "matches": [
            {
                "bashoId": "202401",
                "division": "Makuuchi",
                "day": 15,
                "matchNo": 19,
                "eastId": 1,
                "eastShikona": "Takakeisho",
                "eastRank": "Ozeki 1 East",
                "westId": 45,
                "westShikona": "Terunofuji",
                "westRank": "Komusubi 1 East",
                "kimarite": "abisetaoshi",
                "winnerId": 45,
                "winnerEn": "Terunofuji",
                "winnerJp": "",
            }
        ],
        "kimariteLosses": {"abisetaoshi": 1, "hatakikomi": 2},
        "kimariteWins": {"oshidashi": 4, "tsukiotoshi": 1},
        "opponentWins": 8,
        "rikishiWins": 5,
        "total": 13,
    }

    async with SumoClient() as client:
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ):
            response = await client.get_rikishi_opponent_matches(1, 45)

    assert isinstance(response, RikishiOpponentMatchesResponse)
    assert response.total == TEST_TOTAL_MATCHES
    assert response.rikishi_wins == TEST_RIKISHI_WINS
    assert response.opponent_wins == TEST_OPPONENT_WINS
    assert len(response.matches) == 1
    assert response.kimarite_wins == {"oshidashi": 4, "tsukiotoshi": 1}
    assert response.kimarite_losses == {"abisetaoshi": 1, "hatakikomi": 2}

    first_match = response.matches[0]
    assert isinstance(first_match, Match)
    assert first_match.basho_id == "202401"
    assert first_match.division == "Makuuchi"
    assert first_match.day == TEST_DAY
    assert first_match.match_no == TEST_MATCH_NO
    assert first_match.east_id == 1
    assert first_match.east_shikona == "Takakeisho"
    assert first_match.east_rank == "Ozeki 1 East"
    assert first_match.west_id == TEST_WEST_ID
    assert first_match.west_shikona == "Terunofuji"
    assert first_match.west_rank == "Komusubi 1 East"
    assert first_match.kimarite == "abisetaoshi"
    assert first_match.winner_id == TEST_WINNER_ID
    assert first_match.winner_en == "Terunofuji"
    assert first_match.winner_jp == ""
