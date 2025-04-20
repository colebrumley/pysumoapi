"""Tests for torikumi endpoints."""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest
from zoneinfo import ZoneInfo

from pysumoapi.client import SumoClient
from pysumoapi.models import Match, Torikumi, YushoWinner


@pytest.mark.asyncio
async def test_get_torikumi_success():
    """Test getting torikumi for a specific basho, division, and day."""
    mock_response = {
        "bashoId": "202401",
        "division": "Makuuchi",
        "day": 1,
        "date": "2024-01-14",
        "location": "Ryogoku Kokugikan",
        "startDate": "2024-01-14T00:00:00Z",
        "endDate": "2024-01-28T00:00:00Z",
        "torikumi": [
            {
                "id": "202401-1-1-1-2",
                "bashoId": "202401",
                "division": "Makuuchi",
                "day": 1,
                "matchNo": 1,
                "eastId": 1,
                "eastShikona": "Test Rikishi",
                "eastRank": "M1e",
                "westId": 2,
                "westShikona": "Test Opponent",
                "westRank": "M1w",
                "kimarite": "yorikiri",
                "winnerId": 1,
                "winnerEn": "Test Rikishi",
                "winnerJp": "テスト力士",
                "date": "2024-01-14T00:00:00Z",
            }
        ],
        "specialPrizes": [
            {
                "type": "Shukun-sho",
                "rikishiId": "1",
                "shikonaEn": "Test Rikishi",
                "shikonaJp": "テスト力士",
            }
        ],
    }

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            result = await client.get_torikumi("202401", "Makuuchi", 1)

    assert isinstance(result, Torikumi)
    assert result.basho_id == "202401"
    assert result.division == "Makuuchi"
    assert result.day == 1
    assert result.date == "2024-01-14"
    assert result.location == "Ryogoku Kokugikan"
    assert result.start_date == datetime(2024, 1, 14, tzinfo=ZoneInfo("UTC"))
    assert result.end_date == datetime(2024, 1, 28, tzinfo=ZoneInfo("UTC"))
    assert len(result.matches) == 1
    assert len(result.special_prizes) == 1

    match = result.matches[0]
    assert isinstance(match, Match)
    assert match.id == "202401-1-1-1-2"
    assert match.basho_id == "202401"
    assert match.division == "Makuuchi"
    assert match.day == 1
    assert match.match_no == 1
    assert match.east_id == 1
    assert match.east_shikona == "Test Rikishi"
    assert match.east_rank == "M1e"
    assert match.west_id == 2
    assert match.west_shikona == "Test Opponent"
    assert match.west_rank == "M1w"
    assert match.kimarite == "yorikiri"
    assert match.winner_id == 1
    assert match.winner_en == "Test Rikishi"
    assert match.winner_jp == "テスト力士"

    prize = result.special_prizes[0]
    assert prize.type == "Shukun-sho"
    assert prize.rikishi_id == "1"
    assert prize.shikona_en == "Test Rikishi"
    assert prize.shikona_jp == "テスト力士"


@pytest.mark.asyncio
async def test_get_torikumi_invalid_basho():
    """Test getting torikumi with an invalid basho ID."""
    with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
        async with SumoClient() as client:
            await client.get_torikumi("invalid", "Makuuchi", 1)


@pytest.mark.asyncio
async def test_get_torikumi_invalid_division():
    """Test getting torikumi with an invalid division."""
    with pytest.raises(ValueError, match="Invalid division"):
        async with SumoClient() as client:
            await client.get_torikumi("202401", "Invalid", 1)


@pytest.mark.asyncio
async def test_get_torikumi_invalid_day():
    """Test getting torikumi with an invalid day."""
    with pytest.raises(ValueError, match="Day must be between 1 and 15"):
        async with SumoClient() as client:
            await client.get_torikumi("202401", "Makuuchi", 0)


@pytest.mark.asyncio
async def test_get_torikumi_future_date():
    """Test handling of future basho dates."""
    async with SumoClient() as client:
        future_date = (datetime.now().replace(day=1) + timedelta(days=32)).strftime(
            "%Y%m"
        )
        with pytest.raises(ValueError, match="Cannot fetch future basho"):
            await client.get_torikumi(future_date, "Makuuchi", 1)
