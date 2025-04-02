import pytest
from datetime import datetime, timezone, timedelta
from pysumoapi.client import SumoClient
from pysumoapi.models.torikumi import Torikumi, Match, YushoWinner


@pytest.mark.asyncio
async def test_get_torikumi_success():
    """Test successful retrieval of torikumi details."""
    async with SumoClient() as client:
        torikumi = await client.get_torikumi("202305", "Makuuchi", 1)
        
        assert isinstance(torikumi, Torikumi)
        assert torikumi.date == "202305"
        assert torikumi.location == "Tokyo, Ryogoku Kokugikan"
        assert torikumi.start_date == datetime(2023, 5, 14, tzinfo=timezone.utc)
        assert torikumi.end_date == datetime(2023, 5, 28, tzinfo=timezone.utc)
        
        # Test yusho winners
        assert len(torikumi.yusho) > 0
        first_winner = torikumi.yusho[0]
        assert isinstance(first_winner, YushoWinner)
        assert first_winner.type == "Makuuchi"
        assert first_winner.rikishi_id > 0
        assert first_winner.shikona_en
        assert first_winner.shikona_jp
        
        # Test matches
        assert len(torikumi.matches) > 0
        first_match = torikumi.matches[0]
        assert isinstance(first_match, Match)
        assert first_match.basho_id == "202305"
        assert first_match.division == "Makuuchi"
        assert first_match.day == 1
        assert first_match.match_no > 0
        assert first_match.east_id > 0
        assert first_match.east_shikona
        assert first_match.east_rank
        assert first_match.west_id > 0
        assert first_match.west_shikona
        assert first_match.west_rank
        assert first_match.kimarite
        assert first_match.winner_id > 0
        assert first_match.winner_en
        assert first_match.winner_jp is not None


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
        with pytest.raises(ValueError, match="Day must be between 1 and 15"):
            await client.get_torikumi("202305", "Makuuchi", 16)


@pytest.mark.asyncio
async def test_get_torikumi_future_date():
    """Test handling of future basho dates."""
    async with SumoClient() as client:
        future_date = (datetime.now().replace(day=1) + timedelta(days=32)).strftime("%Y%m")
        with pytest.raises(ValueError, match="Cannot fetch future basho"):
            await client.get_torikumi(future_date, "Makuuchi", 1) 