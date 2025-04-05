from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from pysumoapi.client import SumoClient
from pysumoapi.models import Match, Torikumi, YushoWinner


@pytest.mark.asyncio
async def test_get_torikumi_success():
    """Test successful retrieval of torikumi details."""
    mock_response = {
        "bashoId": "202305",
        "division": "Makuuchi",
        "day": 1,
        "date": "202305",
        "location": "Tokyo",
        "startDate": "2023-05-14T00:00:00Z",
        "endDate": "2023-05-28T00:00:00Z",
        "torikumi": [
            {
                "id": "202305-1-1-29-41",
                "bashoId": "202305",
                "division": "Makuuchi",
                "day": 1,
                "matchNo": 1,
                "eastId": 29,
                "eastShikona": "Takakeisho",
                "eastRank": "Ozeki 1 East",
                "westId": 41,
                "westShikona": "Terunofuji",
                "westRank": "Yokozuna 1 East",
                "kimarite": "oshidashi",
                "winnerId": 41,
                "winnerEn": "Terunofuji",
                "winnerJp": "照ノ富士",
            }
        ],
        "yushoWinners": [
            {
                "id": "41",
                "shikonaEn": "Terunofuji",
                "shikonaJp": "照ノ富士",
                "rank": "Yokozuna 1 East",
                "record": "15-0",
            }
        ],
        "specialPrizes": [
            {
                "type": "Shukun-sho",
                "rikishiId": "29",
                "shikonaEn": "Takakeisho",
                "shikonaJp": "貴景勝",
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
            torikumi = await client.get_torikumi("202305", "Makuuchi", 1)

            # Verify response type
            assert isinstance(torikumi, Torikumi)

            # Verify basic fields
            assert torikumi.basho_id == "202305"
            assert torikumi.division == "Makuuchi"
            assert torikumi.day == 1
            assert torikumi.date == "202305"
            assert torikumi.location == "Tokyo"
            assert torikumi.start_date == datetime(2023, 5, 14, tzinfo=timezone.utc)
            assert torikumi.end_date == datetime(2023, 5, 28, tzinfo=timezone.utc)

            # Verify matches
            assert len(torikumi.matches) == 1
            match = torikumi.matches[0]
            assert isinstance(match, Match)
            assert match.id == "202305-1-1-29-41"
            assert match.match_no == 1
            assert match.east_id == 29
            assert match.east_shikona == "Takakeisho"
            assert match.east_rank == "Ozeki 1 East"
            assert match.west_id == 41
            assert match.west_shikona == "Terunofuji"
            assert match.west_rank == "Yokozuna 1 East"
            assert match.kimarite == "oshidashi"
            assert match.winner_id == 41
            assert match.winner_en == "Terunofuji"
            assert match.winner_jp == "照ノ富士"

            # Verify yusho winner
            assert len(torikumi.yusho_winners) == 1
            yusho_winner = torikumi.yusho_winners[0]
            assert isinstance(yusho_winner, YushoWinner)
            assert yusho_winner.id == "41"
            assert yusho_winner.shikona_en == "Terunofuji"
            assert yusho_winner.shikona_jp == "照ノ富士"
            assert yusho_winner.rank == "Yokozuna 1 East"
            assert yusho_winner.record == "15-0"

            # Verify special prizes
            assert len(torikumi.special_prizes) == 1
            special_prize = torikumi.special_prizes[0]
            assert special_prize.type == "Shukun-sho"
            assert special_prize.rikishi_id == "29"
            assert special_prize.shikona_en == "Takakeisho"
            assert special_prize.shikona_jp == "貴景勝"


@pytest.mark.asyncio
async def test_get_torikumi_invalid_id():
    """Test handling of invalid basho ID format."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Basho ID must be in YYYYMM format"):
            await client.get_torikumi("invalid", "Makuuchi", 1)


@pytest.mark.asyncio
async def test_get_torikumi_invalid_division():
    """Test handling of invalid division."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Invalid division"):
            await client.get_torikumi("202305", "Invalid", 1)


@pytest.mark.asyncio
async def test_get_torikumi_invalid_day():
    """Test handling of invalid day."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Day must be between 1 and 15"):
            await client.get_torikumi("202305", "Makuuchi", 0)


@pytest.mark.asyncio
async def test_get_torikumi_future_date():
    """Test handling of future basho dates."""
    async with SumoClient() as client:
        future_date = (datetime.now().replace(day=1) + timedelta(days=32)).strftime(
            "%Y%m"
        )
        with pytest.raises(ValueError, match="Cannot fetch future basho"):
            await client.get_torikumi(future_date, "Makuuchi", 1)
