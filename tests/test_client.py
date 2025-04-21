"""
Tests for the Sumo API client.
"""

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from zoneinfo import ZoneInfo
import httpx

from pysumoapi.client import SumoClient
from pysumoapi.models import DivisionStats, Rikishi, RikishiList, RikishiStats, Sansho

# Test constants
TEST_DEFAULT_LIMIT = 10
TEST_CUSTOM_LIMIT = 50
TEST_SKIP = 10
TEST_HEIGHT = 180
TEST_WEIGHT = 150
TEST_RIKISHI_ID = 1
TEST_SUMODB_ID = 123
TEST_NSK_ID = 456
TEST_TOTAL_MATCHES = 80
TEST_TOTAL_WINS = 39
TEST_TOTAL_LOSSES = 41
TEST_TOTAL_BASHO = 10
TEST_TOTAL_ABSENCES = 1
TEST_YUSHO = 1
TEST_KANTO_SHO = 2
TEST_GINO_SHO = 1
TEST_SHUKUN_SHO = 1
TEST_MAKUUCHI_MATCHES = 30
TEST_MAKUUCHI_WINS = 15
TEST_MAKUUCHI_LOSSES = 15
TEST_JURYO_MATCHES = 20
TEST_JURYO_WINS = 10
TEST_JURYO_LOSSES = 10
TEST_MAKUSHITA_MATCHES = 15
TEST_MAKUSHITA_WINS = 7
TEST_MAKUSHITA_LOSSES = 8
TEST_JONIDAN_MATCHES = 10
TEST_JONIDAN_WINS = 5
TEST_JONIDAN_LOSSES = 5
TEST_JONOKUCHI_MATCHES = 5
TEST_JONOKUCHI_WINS = 2
TEST_JONOKUCHI_LOSSES = 3


@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    with patch("httpx.AsyncClient") as mock:
        client = mock.return_value
        client.__aenter__.return_value = client
        client.__aexit__.return_value = None
        client.request = AsyncMock()
        client.aclose = AsyncMock()
        yield client


@pytest.fixture
def mock_rikishi_response():
    """Create a mock response for the rikishi endpoint."""
    return {
        "id": TEST_RIKISHI_ID,
        "sumodbId": TEST_SUMODB_ID,
        "nskId": TEST_NSK_ID,
        "shikonaEn": "Test Rikishi",
        "shikonaJp": "テスト力士",
        "currentRank": "M1",
        "heya": "Test Stable",
        "birthDate": "1990-01-01T00:00:00Z",
        "shusshin": "Tokyo",
        "height": TEST_HEIGHT,
        "weight": TEST_WEIGHT,
        "debut": "2010-01",
        "updatedAt": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_rikishi_stats_response():
    """Create a mock response for the rikishi stats endpoint."""
    return {
        "basho": TEST_TOTAL_BASHO,
        "totalMatches": TEST_TOTAL_MATCHES,
        "totalWins": TEST_TOTAL_WINS,
        "totalLosses": TEST_TOTAL_LOSSES,
        "totalAbsences": TEST_TOTAL_ABSENCES,
        "yusho": TEST_YUSHO,
        "absenceByDivision": {
            "Jonidan": 0,
            "Jonokuchi": 0,
            "Juryo": 0,
            "Makushita": 0,
            "Makuuchi": TEST_TOTAL_ABSENCES,
            "Sandanme": 0,
        },
        "bashoByDivision": {
            "Jonidan": 2,
            "Jonokuchi": 1,
            "Juryo": 3,
            "Makushita": 2,
            "Makuuchi": 2,
            "Sandanme": 0,
        },
        "lossByDivision": {
            "Jonidan": TEST_JONIDAN_LOSSES,
            "Jonokuchi": TEST_JONOKUCHI_LOSSES,
            "Juryo": TEST_JURYO_LOSSES,
            "Makushita": TEST_MAKUSHITA_LOSSES,
            "Makuuchi": TEST_MAKUUCHI_LOSSES,
            "Sandanme": 0,
        },
        "totalByDivision": {
            "Jonidan": TEST_JONIDAN_MATCHES,
            "Jonokuchi": TEST_JONOKUCHI_MATCHES,
            "Juryo": TEST_JURYO_MATCHES,
            "Makushita": TEST_MAKUSHITA_MATCHES,
            "Makuuchi": TEST_MAKUUCHI_MATCHES,
            "Sandanme": 0,
        },
        "winsByDivision": {
            "Jonidan": TEST_JONIDAN_WINS,
            "Jonokuchi": TEST_JONOKUCHI_WINS,
            "Juryo": TEST_JURYO_WINS,
            "Makushita": TEST_MAKUSHITA_WINS,
            "Makuuchi": TEST_MAKUUCHI_WINS,
            "Sandanme": 0,
        },
        "yushoByDivision": {
            "Jonidan": 0,
            "Jonokuchi": 0,
            "Juryo": TEST_YUSHO,
            "Makushita": 0,
            "Makuuchi": 0,
            "Sandanme": 0,
        },
        "sansho": {
            "Gino-sho": TEST_GINO_SHO,
            "Kanto-sho": TEST_KANTO_SHO,
            "Shukun-sho": TEST_SHUKUN_SHO,
        },
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
                "id": TEST_RIKISHI_ID,
                "sumodbId": TEST_SUMODB_ID,
                "nskId": TEST_NSK_ID,
                "shikonaEn": "Test Rikishi",
                "shikonaJp": "テスト力士",
                "currentRank": "M1",
                "heya": "Test Stable",
                "birthDate": "1990-01-01T00:00:00Z",
                "shusshin": "Tokyo",
                "height": TEST_HEIGHT,
                "weight": TEST_WEIGHT,
                "debut": "2010-01",
                "updatedAt": "2024-01-01T00:00:00Z",
            }
        ],
    }


@pytest.mark.asyncio
async def test_get_rikishi(mock_client, mock_rikishi_response):
    """Test getting a single rikishi."""
    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_rikishi_response):
            rikishi = await client.get_rikishi("1")

    assert isinstance(rikishi, Rikishi)
    assert rikishi.id == TEST_RIKISHI_ID
    assert rikishi.shikona_en == "Test Rikishi"
    assert rikishi.current_rank == "M1"
    assert rikishi.heya == "Test Stable"
    assert rikishi.birth_date == datetime(1990, 1, 1, tzinfo=ZoneInfo("UTC"))
    assert rikishi.shusshin == "Tokyo"
    assert rikishi.height == TEST_HEIGHT
    assert rikishi.weight == TEST_WEIGHT
    assert rikishi.debut == "2010-01"
    assert rikishi.updated_at == datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))


@pytest.mark.asyncio
async def test_get_rikishi_stats(mock_client, mock_rikishi_stats_response):
    """Test getting rikishi stats."""
    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_rikishi_stats_response):
            stats = await client.get_rikishi_stats("1")

    assert isinstance(stats, RikishiStats)
    assert stats.basho == TEST_TOTAL_BASHO
    assert stats.total_matches == TEST_TOTAL_MATCHES
    assert stats.total_wins == TEST_TOTAL_WINS
    assert stats.total_losses == TEST_TOTAL_LOSSES
    assert stats.total_absences == TEST_TOTAL_ABSENCES
    assert stats.yusho == TEST_YUSHO
    assert stats.sansho.Gino_sho == TEST_GINO_SHO
    assert stats.sansho.Kanto_sho == TEST_KANTO_SHO
    assert stats.sansho.Shukun_sho == TEST_SHUKUN_SHO


@pytest.mark.asyncio
async def test_get_rikishis(mock_client, mock_rikishis_response):
    """Test getting a list of rikishi."""
    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_rikishis_response):
            rikishis = await client.get_rikishis()

    assert isinstance(rikishis, RikishiList)
    assert rikishis.limit == TEST_DEFAULT_LIMIT
    assert rikishis.skip == 0
    assert rikishis.total == 1
    assert len(rikishis.records) == 1

    rikishi = rikishis.records[0]
    assert isinstance(rikishi, Rikishi)
    assert rikishi.id == TEST_RIKISHI_ID
    assert rikishi.shikona_en == "Test Rikishi"
    assert rikishi.current_rank == "M1"
    assert rikishi.heya == "Test Stable"
    assert rikishi.birth_date == datetime(1990, 1, 1, tzinfo=ZoneInfo("UTC"))
    assert rikishi.shusshin == "Tokyo"
    assert rikishi.height == TEST_HEIGHT
    assert rikishi.weight == TEST_WEIGHT
    assert rikishi.debut == "2010-01"
    assert rikishi.updated_at == datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))


@pytest.mark.asyncio
async def test_get_rikishis_with_filters(mock_client, mock_rikishis_response):
    """Test getting a list of rikishi with filters."""
    async with SumoClient() as client:
        with patch.object(client, "_make_request", return_value=mock_rikishis_response):
            rikishis = await client.get_rikishis(
                shikona_en="Test",
                heya="Test Stable",
                sumodb_id=TEST_SUMODB_ID,
                nsk_id=TEST_NSK_ID,
                intai=False,
                measurements=True,
                ranks=True,
                shikonas=True,
                limit=TEST_CUSTOM_LIMIT,
                skip=TEST_SKIP,
            )

    assert isinstance(rikishis, RikishiList)
    assert rikishis.limit == TEST_DEFAULT_LIMIT
    assert rikishis.skip == 0
    assert rikishis.total == 1
    assert len(rikishis.records) == 1

    rikishi = rikishis.records[0]
    assert isinstance(rikishi, Rikishi)
    assert rikishi.id == TEST_RIKISHI_ID
    assert rikishi.shikona_en == "Test Rikishi"
    assert rikishi.current_rank == "M1"
    assert rikishi.heya == "Test Stable"
    assert rikishi.birth_date == datetime(1990, 1, 1, tzinfo=ZoneInfo("UTC"))
    assert rikishi.shusshin == "Tokyo"
    assert rikishi.height == TEST_HEIGHT
    assert rikishi.weight == TEST_WEIGHT
    assert rikishi.debut == "2010-01"
    assert rikishi.updated_at == datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))


@pytest.mark.asyncio
async def test_client_initialization():
    """Test client initialization with default values."""
    client = SumoClient()
    assert client.base_url == "https://sumo-api.com/api"
    assert client.timeout is None
    assert client.retries == 3
    assert client._client is None


@pytest.mark.asyncio
async def test_client_context_manager(mock_client):
    """Test client context manager."""
    mock_client.base_url = "https://sumo.com/api"
    mock_client.timeout = None
    mock_client.transport.retries = 3

    async with SumoClient() as client:
        assert client._client is not None
        assert isinstance(client._client, mock_client.__class__)
        assert client._client.base_url == "https://sumo.com/api"
        assert client._client.timeout is None
        assert client._client.transport.retries == 3

    assert client._client is None
