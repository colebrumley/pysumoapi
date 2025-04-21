"""Tests for rikishi matches endpoints."""

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from zoneinfo import ZoneInfo

from pysumoapi.client import SumoClient
from pysumoapi.models import Match, RikishiMatchesResponse


@pytest.mark.asyncio
async def test_get_rikishi_matches_success():
    """Test getting matches for a rikishi."""
    mock_response = {
        "limit": 10,
        "skip": 0,
        "total": 1,
        "records": [
            {
                "bashoId": "202401",
                "division": "Makuuchi",
                "day": 1,
                "rikishiId": 1,
                "rikishiShikona": "Test Rikishi",
                "opponentId": 2,
                "opponentShikona": "Test Opponent",
                "kimarite": "yorikiri",
                "winner": True,
                "date": "2024-01-14T00:00:00Z",
            }
        ],
    }

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            result = await client.get_rikishi_matches(1, "202401")

    assert isinstance(result, RikishiMatchesResponse)
    assert result.limit == 10
    assert result.skip == 0
    assert result.total == 1
    assert len(result.records) == 1

    match = result.records[0]
    assert isinstance(match, Match)
    assert match.basho_id == "202401"
    assert match.division == "Makuuchi"
    assert match.day == 1
    assert match.rikishi_id == 1
    assert match.rikishi_shikona == "Test Rikishi"
    assert match.opponent_id == 2
    assert match.opponent_shikona == "Test Opponent"
    assert match.kimarite == "yorikiri"
    assert match.winner is True
    assert match.date == datetime(2024, 1, 14, tzinfo=ZoneInfo("UTC"))


@pytest.mark.asyncio
async def test_get_rikishi_matches_no_basho():
    """Test getting all matches for a rikishi without specifying a basho."""
    mock_response = {
        "limit": 10,
        "skip": 0,
        "total": 1,
        "records": [
            {
                "bashoId": "202401",
                "division": "Makuuchi",
                "day": 1,
                "rikishiId": 1,
                "rikishiShikona": "Test Rikishi",
                "opponentId": 2,
                "opponentShikona": "Test Opponent",
                "kimarite": "yorikiri",
                "winner": True,
                "date": "2024-01-14T00:00:00Z",
            }
        ],
    }

    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_response):
            result = await client.get_rikishi_matches(1)

    assert isinstance(result, RikishiMatchesResponse)
    assert result.limit == 10
    assert result.skip == 0
    assert result.total == 1
    assert len(result.records) == 1

    match = result.records[0]
    assert isinstance(match, Match)
    assert match.basho_id == "202401"
    assert match.division == "Makuuchi"
    assert match.day == 1
    assert match.rikishi_id == 1
    assert match.rikishi_shikona == "Test Rikishi"
    assert match.opponent_id == 2
    assert match.opponent_shikona == "Test Opponent"
    assert match.kimarite == "yorikiri"
    assert match.winner is True
    assert match.date == datetime(2024, 1, 14, tzinfo=ZoneInfo("UTC"))


@pytest.mark.asyncio
async def test_get_rikishi_matches_invalid_id():
    """Test getting matches with an invalid rikishi ID."""
    with pytest.raises(ValueError, match="Rikishi ID must be positive"):
        async with SumoClient() as client:
            await client.get_rikishi_matches(0)


@pytest.mark.asyncio
async def test_get_rikishi_matches_invalid_basho():
    """Test getting matches with an invalid basho ID."""
    with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
        async with SumoClient() as client:
            await client.get_rikishi_matches(1, "invalid")
