import pytest
from pysumoapi.client import SumoClient
from pysumoapi.models.kimarite import KimariteMatchesResponse


@pytest.mark.asyncio
async def test_get_kimarite_matches_success():
    """Test successful retrieval of kimarite matches."""
    async with SumoClient() as client:
        response = await client.get_kimarite_matches(
            kimarite="yorikiri",
            sort_order="desc",
            limit=5
        )
        
        # Verify response type
        assert isinstance(response, KimariteMatchesResponse)
        
        # Verify query parameters are reflected
        assert response.limit == 5
        assert response.skip == 0
        assert response.total > 0
        
        # Verify records
        assert len(response.records) == 5
        for match in response.records:
            assert match.kimarite == "yorikiri"
            assert match.basho_id
            assert 1 <= match.day <= 15
            assert match.match_no > 0
            assert match.east_id
            assert match.east_shikona
            assert match.east_rank
            assert match.west_id
            assert match.west_shikona
            assert match.west_rank
            assert match.winner_id
            assert match.winner_en
            assert match.winner_jp
            
        # Verify sorting (by basho and day)
        basho_days = [(m.basho_id, m.day) for m in response.records]
        assert basho_days == sorted(basho_days, reverse=True)


@pytest.mark.asyncio
async def test_get_kimarite_matches_invalid_kimarite():
    """Test handling of invalid kimarite."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Kimarite cannot be empty"):
            await client.get_kimarite_matches("")


@pytest.mark.asyncio
async def test_get_kimarite_matches_invalid_sort_order():
    """Test handling of invalid sort order."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Sort order must be either 'asc' or 'desc'"):
            await client.get_kimarite_matches("yorikiri", sort_order="invalid")


@pytest.mark.asyncio
async def test_get_kimarite_matches_invalid_limit():
    """Test handling of invalid limit."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Limit must be a positive integer"):
            await client.get_kimarite_matches("yorikiri", limit=-1)
        
        with pytest.raises(ValueError, match="Limit cannot exceed 1000"):
            await client.get_kimarite_matches("yorikiri", limit=1001)


@pytest.mark.asyncio
async def test_get_kimarite_matches_invalid_skip():
    """Test handling of invalid skip."""
    async with SumoClient() as client:
        with pytest.raises(ValueError, match="Skip must be a non-negative integer"):
            await client.get_kimarite_matches("yorikiri", skip=-1) 