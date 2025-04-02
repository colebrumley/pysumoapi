"""
Tests for the Sumo API client.
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

from pysumoapi.client import SumoClient
from pysumoapi.models import Rikishi, RikishiList, RikishiStats, DivisionStats, Sansho


@pytest.fixture
def mock_transport():
    """Create a mock transport for testing."""
    with patch("httpx.AsyncClient") as mock:
        client = mock.return_value
        client.__aenter__.return_value = client
        client.__aexit__.return_value = None
        client.get = AsyncMock()
        client.aclose = AsyncMock()
        yield client


@pytest.fixture
def mock_rikishi_response():
    """Create a mock response for the rikishi endpoint."""
    return {
        "id": 1,
        "sumodbId": 123,
        "nskId": 456,
        "shikonaEn": "Test Rikishi",
        "shikonaJp": "テスト力士",
        "currentRank": "M1",
        "heya": "Test Stable",
        "birthDate": "1990-01-01T00:00:00Z",
        "shusshin": "Tokyo",
        "height": 180,
        "weight": 150,
        "debut": "2010-01",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_rikishi_stats_response():
    """Create a mock response for the rikishi stats endpoint."""
    return {
        "absenceByDivision": {
            "Jonidan": 0,
            "Jonokuchi": 0,
            "Juryo": 0,
            "Makushita": 0,
            "Makuuchi": 1,
            "Sandanme": 0
        },
        "basho": 10,
        "bashoByDivision": {
            "Jonidan": 2,
            "Jonokuchi": 1,
            "Juryo": 3,
            "Makushita": 2,
            "Makuuchi": 2,
            "Sandanme": 0
        },
        "lossByDivision": {
            "Jonidan": 5,
            "Jonokuchi": 3,
            "Juryo": 10,
            "Makushita": 8,
            "Makuuchi": 15,
            "Sandanme": 0
        },
        "sansho": {
            "Gino-sho": 1,
            "Kanto-sho": 2,
            "Shukun-sho": 1
        },
        "totalAbsences": 1,
        "totalByDivision": {
            "Jonidan": 10,
            "Jonokuchi": 5,
            "Juryo": 20,
            "Makushita": 15,
            "Makuuchi": 30,
            "Sandanme": 0
        },
        "totalLosses": 41,
        "totalMatches": 80,
        "totalWins": 39,
        "winsByDivision": {
            "Jonidan": 5,
            "Jonokuchi": 2,
            "Juryo": 10,
            "Makushita": 7,
            "Makuuchi": 15,
            "Sandanme": 0
        },
        "yusho": 1,
        "yushoByDivision": {
            "Jonidan": 0,
            "Jonokuchi": 0,
            "Juryo": 1,
            "Makushita": 0,
            "Makuuchi": 0,
            "Sandanme": 0
        }
    }


@pytest.fixture
def mock_rikishis_response():
    """Create a mock response for the rikishis endpoint."""
    return {
        "limit": 10,
        "skip": 0,
        "total": 1,
        "records": [
            {
                "id": 1,
                "sumodbId": 123,
                "nskId": 456,
                "shikonaEn": "Test Rikishi",
                "shikonaJp": "テスト力士",
                "currentRank": "M1",
                "heya": "Test Stable",
                "birthDate": "1990-01-01T00:00:00Z",
                "shusshin": "Tokyo",
                "height": 180,
                "weight": 150,
                "debut": "2010-01",
                "updatedAt": "2024-01-01T00:00:00Z",
            }
        ],
    }


@pytest.mark.asyncio
async def test_get_rikishi():
    """Test getting a single rikishi."""
    mock_response = {
        "id": 1,
        "sumodbId": 123,
        "nskId": 456,
        "shikonaEn": "Test Rikishi",
        "shikonaJp": "テスト力士",
        "currentRank": "M1",
        "heya": "Test Stable",
        "birthDate": "1990-01-01T00:00:00Z",
        "shusshin": "Tokyo",
        "height": 180,
        "weight": 150,
        "debut": "2010-01",
        "updatedAt": "2024-01-01T00:00:00Z",
    }
    
    async with SumoClient() as client:
        with patch.object(client._client, "request", return_value=AsyncMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )):
            rikishi = await client.get_rikishi("1")
            
    assert isinstance(rikishi, Rikishi)
    assert rikishi.id == 1
    assert rikishi.shikona_en == "Test Rikishi"
    assert rikishi.current_rank == "M1"
    assert rikishi.heya == "Test Stable"
    assert rikishi.birth_date == datetime(1990, 1, 1, tzinfo=ZoneInfo("UTC"))
    assert rikishi.shusshin == "Tokyo"
    assert rikishi.height == 180
    assert rikishi.weight == 150
    assert rikishi.debut == "2010-01"
    assert rikishi.updated_at == datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))


@pytest.mark.asyncio
async def test_get_rikishi_stats():
    """Test getting a rikishi's statistics."""
    mock_response = {
        "basho": 10,
        "totalMatches": 80,
        "totalWins": 39,
        "totalLosses": 41,
        "totalAbsences": 1,
        "yusho": 1,
        "absenceByDivision": {
            "Jonidan": 0,
            "Jonokuchi": 0,
            "Juryo": 0,
            "Makushita": 0,
            "Makuuchi": 1,
            "Sandanme": 0
        },
        "bashoByDivision": {
            "Jonidan": 2,
            "Jonokuchi": 1,
            "Juryo": 3,
            "Makushita": 2,
            "Makuuchi": 2,
            "Sandanme": 0
        },
        "lossByDivision": {
            "Jonidan": 5,
            "Jonokuchi": 3,
            "Juryo": 10,
            "Makushita": 8,
            "Makuuchi": 15,
            "Sandanme": 0
        },
        "totalByDivision": {
            "Jonidan": 10,
            "Jonokuchi": 5,
            "Juryo": 20,
            "Makushita": 15,
            "Makuuchi": 30,
            "Sandanme": 0
        },
        "winsByDivision": {
            "Jonidan": 5,
            "Jonokuchi": 2,
            "Juryo": 10,
            "Makushita": 7,
            "Makuuchi": 15,
            "Sandanme": 0
        },
        "yushoByDivision": {
            "Jonidan": 0,
            "Jonokuchi": 0,
            "Juryo": 1,
            "Makushita": 0,
            "Makuuchi": 0,
            "Sandanme": 0
        },
        "sansho": {
            "Gino-sho": 1,
            "Kanto-sho": 2,
            "Shukun-sho": 1
        }
    }
    
    async with SumoClient() as client:
        with patch.object(client._client, "request", return_value=AsyncMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )):
            stats = await client.get_rikishi_stats("1")
            
    assert isinstance(stats, RikishiStats)
    assert stats.basho == 10
    assert stats.total_matches == 80
    assert stats.total_wins == 39
    assert stats.total_losses == 41
    assert stats.total_absences == 1
    assert stats.yusho == 1
    
    # Test division stats
    assert isinstance(stats.absence_by_division, DivisionStats)
    assert stats.absence_by_division.Makuuchi == 1
    assert stats.absence_by_division.Juryo == 0
    
    # Test sansho (special prizes)
    assert isinstance(stats.sansho, Sansho)
    assert stats.sansho.Gino_sho == 1
    assert stats.sansho.Kanto_sho == 2
    assert stats.sansho.Shukun_sho == 1


@pytest.mark.asyncio
async def test_get_rikishis():
    """Test getting a list of rikishi."""
    mock_response = {
        "limit": 10,
        "skip": 0,
        "total": 1,
        "records": [
            {
                "id": 1,
                "sumodbId": 123,
                "nskId": 456,
                "shikonaEn": "Test Rikishi",
                "shikonaJp": "テスト力士",
                "currentRank": "M1",
                "heya": "Test Stable",
                "birthDate": "1990-01-01T00:00:00Z",
                "shusshin": "Tokyo",
                "height": 180,
                "weight": 150,
                "debut": "2010-01",
                "updatedAt": "2024-01-01T00:00:00Z",
            }
        ],
    }
    
    async with SumoClient() as client:
        with patch.object(client._client, "request", return_value=AsyncMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )):
            result = await client.get_rikishis()
            
    assert isinstance(result, RikishiList)
    assert result.limit == 10
    assert result.skip == 0
    assert result.total == 1
    assert len(result.records) == 1
    
    rikishi = result.records[0]
    assert isinstance(rikishi, Rikishi)
    assert rikishi.id == 1
    assert rikishi.shikona_en == "Test Rikishi"
    assert rikishi.current_rank == "M1"
    assert rikishi.heya == "Test Stable"
    assert rikishi.birth_date == datetime(1990, 1, 1, tzinfo=ZoneInfo("UTC"))
    assert rikishi.shusshin == "Tokyo"
    assert rikishi.height == 180
    assert rikishi.weight == 150
    assert rikishi.debut == "2010-01"
    assert rikishi.updated_at == datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))


@pytest.mark.asyncio
async def test_get_rikishis_with_filters():
    """Test getting a list of rikishi with filters."""
    mock_response = {
        "limit": 50,
        "skip": 10,
        "total": 1,
        "records": [
            {
                "id": 1,
                "sumodbId": 123,
                "nskId": 456,
                "shikonaEn": "Test Rikishi",
                "shikonaJp": "テスト力士",
                "currentRank": "M1",
                "heya": "Test Stable",
                "birthDate": "1990-01-01T00:00:00Z",
                "shusshin": "Tokyo",
                "height": 180,
                "weight": 150,
                "debut": "2010-01",
                "updatedAt": "2024-01-01T00:00:00Z",
            }
        ],
    }
    
    async with SumoClient() as client:
        with patch.object(client._client, "request", return_value=AsyncMock(
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )) as mock_request:
            result = await client.get_rikishis(
                shikona_en="Test",
                heya="Test Stable",
                sumodb_id=123,
                nsk_id=456,
                intai=False,
                measurements=True,
                ranks=True,
                shikonas=True,
                limit=50,
                skip=10,
            )
            
            # Verify the request parameters
            mock_request.assert_called_once_with(
                "GET",
                "https://sumo-api.com/api/rikishis",
                params={
                    "shikonaEn": "Test",
                    "heya": "Test Stable",
                    "sumodbId": 123,
                    "nskId": 456,
                    "intai": "false",
                    "measurements": "true",
                    "ranks": "true",
                    "shikonas": "true",
                    "limit": 50,
                    "skip": 10,
                }
            )
            
    # Verify the response
    assert isinstance(result, RikishiList)
    assert result.limit == 50
    assert result.skip == 10
    assert result.total == 1
    assert len(result.records) == 1 