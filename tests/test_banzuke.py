"""Tests for the banzuke endpoint."""

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from pysumoapi.client import SumoClient
from pysumoapi.models import Banzuke, Match, RikishiBanzuke


@pytest.mark.asyncio
async def test_get_banzuke_success():
    """Test successful retrieval of banzuke details."""
    mock_response = {
        "bashoId": "202305",
        "division": "Makuuchi",
        "east": [
            {
                "id": "1",
                "shikonaEn": "Test Rikishi",
                "shikonaJp": "テスト力士",
                "rank": "Yokozuna",
                "heya": "Test Heya",
                "record": [
                    {
                        "bashoId": "202305",
                        "day": 1,
                        "result": "win",
                        "opponentID": "2",
                        "opponentShikonaEn": "Opponent",
                        "opponentShikonaJp": "対戦相手",
                        "kimarite": "yorikiri",
                    }
                ],
            }
        ],
        "west": [],
    }

    with patch.object(SumoClient, "_make_request", return_value=mock_response):
        async with SumoClient() as client:
            banzuke = await client.get_banzuke("202305", "Makuuchi")

            assert isinstance(banzuke, Banzuke)
            assert banzuke.basho_id == "202305"
            assert banzuke.division == "Makuuchi"
            assert len(banzuke.rikishi) > 0

            # Test first rikishi
            first_rikishi = banzuke.rikishi[0]
            assert isinstance(first_rikishi, RikishiBanzuke)
            assert first_rikishi.id == "1"
            assert first_rikishi.shikona_en == "Test Rikishi"
            assert first_rikishi.shikona_jp == "テスト力士"
            assert first_rikishi.rank == "Yokozuna"
            assert first_rikishi.heya == "Test Heya"
            assert len(first_rikishi.matches) > 0

            # Test first match
            first_match = first_rikishi.matches[0]
            assert isinstance(first_match, Match)
            assert first_match.basho_id == "202305"
            assert first_match.day > 0
            assert first_match.result in [
                "win",
                "loss",
                "absent",
                "fusen loss",
                "fusen win",
            ]
            assert first_match.opponent_id == "2"
            assert first_match.opponent_shikona_en == "Opponent"
            assert first_match.opponent_shikona_jp == "対戦相手"
            assert first_match.kimarite


@pytest.mark.asyncio
async def test_get_banzuke_invalid_id():
    """Test handling of invalid basho ID format."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
            await client.get_banzuke("invalid", "Makuuchi")


@pytest.mark.asyncio
async def test_get_banzuke_invalid_division():
    """Test handling of invalid division."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Invalid division"):
            await client.get_banzuke("202305", "Invalid")


@pytest.mark.asyncio
async def test_get_banzuke_future_date():
    """Test handling of future basho dates."""
    async with SumoClient() as client:
        future_date = (datetime.now().replace(day=1) + timedelta(days=32)).strftime(
            "%Y%m"
        )
        with pytest.raises(ValueError, match="Cannot fetch future basho"):
            await client.get_banzuke(future_date, "Makuuchi")
