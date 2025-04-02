import pytest
from datetime import datetime, timedelta
from pysumoapi.client import SumoClient
from pysumoapi.models.banzuke import Banzuke, RikishiBanzuke, Match


@pytest.mark.asyncio
async def test_get_banzuke_success():
    """Test successful retrieval of banzuke details."""
    async with SumoClient() as client:
        banzuke = await client.get_banzuke("202305", "Makuuchi")
        
        assert isinstance(banzuke, Banzuke)
        assert banzuke.basho_id == "202305"
        assert banzuke.division == "Makuuchi"
        assert len(banzuke.east) > 0
        assert len(banzuke.west) > 0
        
        # Test first rikishi in east side
        first_rikishi = banzuke.east[0]
        assert isinstance(first_rikishi, RikishiBanzuke)
        assert first_rikishi.side == "East"
        assert first_rikishi.rikishi_id > 0
        assert first_rikishi.shikona_en
        assert first_rikishi.rank_value > 0
        assert first_rikishi.rank
        assert len(first_rikishi.record) > 0
        assert first_rikishi.wins >= 0
        assert first_rikishi.losses >= 0
        assert first_rikishi.absences >= 0
        
        # Test first match in record
        first_match = first_rikishi.record[0]
        assert isinstance(first_match, Match)
        assert first_match.result in ["win", "loss"]
        assert first_match.opponent_shikona_en
        assert first_match.opponent_id > 0
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
        future_date = (datetime.now().replace(day=1) + timedelta(days=32)).strftime("%Y%m")
        with pytest.raises(ValueError, match="Cannot fetch future basho"):
            await client.get_banzuke(future_date, "Makuuchi") 