"""Tests for the basho endpoint."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest

from pysumoapi.client import SumoClient
from pysumoapi.models import Basho, RikishiPrize

# Test constants
TEST_YUSHO_COUNT = 2
TEST_SPECIAL_PRIZES_COUNT = 2
TEST_TERUNOFUJI_ID = 45
TEST_GONOYAMA_ID = 56
TEST_MEISEI_ID = 38
TEST_WAKAMOTOHARU_ID = 13


@pytest.mark.asyncio
async def test_get_basho_success():
    """Test successful retrieval of basho details."""
    basho_id = "202305"

    mock_response = {
        "date": "202305",
        "location": "Tokyo, Ryogoku Kokugikan",
        "startDate": "2023-05-14T00:00:00Z",
        "endDate": "2023-05-28T00:00:00Z",
        "yusho": [
            {
                "type": "Makuuchi",
                "rikishiId": 45,
                "shikonaEn": "Terunofuji Haruo",
                "shikonaJp": "照ノ富士　春雄",
            },
            {
                "type": "Juryo",
                "rikishiId": 56,
                "shikonaEn": "Gonoyama Toki",
                "shikonaJp": "豪ノ山　登輝",
            },
        ],
        "specialPrizes": [
            {
                "type": "Shukun-sho",
                "rikishiId": 38,
                "shikonaEn": "Meisei Chikara",
                "shikonaJp": "明生　力",
            },
            {
                "type": "Gino-sho",
                "rikishiId": 13,
                "shikonaEn": "Wakamotoharu Minato",
                "shikonaJp": "若元春　港",
            },
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
            response = await client.get_basho(basho_id)

    assert isinstance(response, Basho)
    assert response.date == "202305"
    assert response.location == "Tokyo, Ryogoku Kokugikan"
    assert response.start_date == datetime(2023, 5, 14, tzinfo=timezone.utc)
    assert response.end_date == datetime(2023, 5, 28, tzinfo=timezone.utc)

    # Test yusho winners
    assert len(response.yusho) == TEST_YUSHO_COUNT
    makuuchi_winner = response.yusho[0]
    assert isinstance(makuuchi_winner, RikishiPrize)
    assert makuuchi_winner.type == "Makuuchi"
    assert makuuchi_winner.rikishi_id == TEST_TERUNOFUJI_ID
    assert makuuchi_winner.shikona_en == "Terunofuji Haruo"
    assert makuuchi_winner.shikona_jp == "照ノ富士　春雄"

    juryo_winner = response.yusho[1]
    assert juryo_winner.type == "Juryo"
    assert juryo_winner.rikishi_id == TEST_GONOYAMA_ID
    assert juryo_winner.shikona_en == "Gonoyama Toki"
    assert juryo_winner.shikona_jp == "豪ノ山　登輝"

    # Test special prizes
    assert len(response.special_prizes) == TEST_SPECIAL_PRIZES_COUNT
    shukun_sho = response.special_prizes[0]
    assert isinstance(shukun_sho, RikishiPrize)
    assert shukun_sho.type == "Shukun-sho"
    assert shukun_sho.rikishi_id == TEST_MEISEI_ID
    assert shukun_sho.shikona_en == "Meisei Chikara"
    assert shukun_sho.shikona_jp == "明生　力"

    gino_sho = response.special_prizes[1]
    assert gino_sho.type == "Gino-sho"
    assert gino_sho.rikishi_id == TEST_WAKAMOTOHARU_ID
    assert gino_sho.shikona_en == "Wakamotoharu Minato"
    assert gino_sho.shikona_jp == "若元春　港"


@pytest.mark.asyncio
async def test_get_basho_invalid_id():
    """Test error handling for invalid basho ID format."""
    async with SumoClient() as client:
        with pytest.raises(ValueError):
            await client.get_basho("invalid")


@pytest.mark.asyncio
async def test_get_basho_future_date():
    """Test error handling for future basho date."""
    future_date = "999901"  # Year 9999
    async with SumoClient() as client:
        with pytest.raises(ValueError):
            await client.get_basho(future_date)
