"""
Tests for the Sumo API client.
"""

import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

import httpx
import pytest
from zoneinfo import ZoneInfo

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
async def test_sumo_client_initialization():
    """Test that SumoClient initializes with custom HTTP configuration."""
    client = SumoClient(
        base_url="https://test-api.com",
        verify_ssl=False,
        connect_timeout=10.0,
        read_timeout=15.0,
        enable_http2=False,
        max_retries=3,
        retry_backoff_factor=2.0,
    )
    
    assert client.base_url == "https://test-api.com"
    assert client.verify_ssl is False
    assert client.connect_timeout == 10.0
    assert client.read_timeout == 15.0
    assert client.enable_http2 is False
    assert client.max_retries == 3
    assert client.retry_backoff_factor == 2.0


@pytest.mark.asyncio
async def test_sumo_client_default_initialization():
    """Test that SumoClient initializes with default values."""
    client = SumoClient()
    
    assert client.base_url == "https://sumo-api.com"
    assert client.verify_ssl is True
    assert client.connect_timeout == 5.0
    assert client.read_timeout == 5.0
    assert client.enable_http2 is True
    assert client.max_retries == 2
    assert client.retry_backoff_factor == 1.0


@pytest.mark.asyncio
async def test_get_rikishi():
    """Test getting a single rikishi."""
    mock_response = {
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

    async with SumoClient() as client:
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ):
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
async def test_get_rikishi_stats():
    """Test getting a rikishi's statistics."""
    mock_response = {
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

    async with SumoClient() as client:
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ):
            stats = await client.get_rikishi_stats("1")

    assert isinstance(stats, RikishiStats)
    assert stats.basho == TEST_TOTAL_BASHO
    assert stats.total_matches == TEST_TOTAL_MATCHES
    assert stats.total_wins == TEST_TOTAL_WINS
    assert stats.total_losses == TEST_TOTAL_LOSSES
    assert stats.total_absences == TEST_TOTAL_ABSENCES
    assert stats.yusho == TEST_YUSHO

    # Test division stats
    assert isinstance(stats.absence_by_division, DivisionStats)
    assert stats.absence_by_division.Makuuchi == TEST_TOTAL_ABSENCES
    assert stats.absence_by_division.Juryo == 0

    # Test sansho (special prizes)
    assert isinstance(stats.sansho, Sansho)
    assert stats.sansho.Gino_sho == TEST_GINO_SHO
    assert stats.sansho.Kanto_sho == TEST_KANTO_SHO
    assert stats.sansho.Shukun_sho == TEST_SHUKUN_SHO


@pytest.mark.asyncio
async def test_get_rikishis():
    """Test getting a list of rikishi."""
    mock_response = {
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

    async with SumoClient() as client:
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ):
            result = await client.get_rikishis()

    assert isinstance(result, RikishiList)
    assert result.limit == TEST_DEFAULT_LIMIT
    assert result.skip == 0
    assert result.total == 1
    assert len(result.records) == 1

    rikishi = result.records[0]
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
async def test_get_rikishis_with_filters():
    """Test getting a list of rikishi with filters."""
    mock_response = {
        "limit": 50,
        "skip": 10,
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

    async with SumoClient() as client:
        with patch.object(
            client._client,
            "request",
            return_value=AsyncMock(
                json=lambda: mock_response, raise_for_status=lambda: None
            ),
        ) as mock_request:
            result = await client.get_rikishis(
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

            # Verify the request parameters
            mock_request.assert_called_once_with(
                "GET",
                "https://sumo-api.com/api/rikishis",
                params={
                    "shikonaEn": "Test",
                    "heya": "Test Stable",
                    "sumodbId": TEST_SUMODB_ID,
                    "nskId": TEST_NSK_ID,
                    "intai": "false",
                    "measurements": "true",
                    "ranks": "true",
                    "shikonas": "true",
                    "limit": TEST_CUSTOM_LIMIT,
                    "skip": TEST_SKIP,
                },
            )

    # Verify the response
    assert isinstance(result, RikishiList)
    assert result.limit == TEST_CUSTOM_LIMIT
    assert result.skip == TEST_SKIP
    assert result.total == 1
    assert len(result.records) == 1


@pytest.mark.asyncio
async def test_retry_logic_with_timeout_exception():
    """Test that timeout exceptions trigger retries."""
    mock_response = {"id": 1, "shikonaEn": "Test"}
    
    async with SumoClient(max_retries=2, retry_backoff_factor=0.1) as client:
        with patch.object(client._client, "request") as mock_request:
            # First two calls raise timeout, third succeeds
            mock_request.side_effect = [
                httpx.TimeoutException("Connection timed out"),
                httpx.TimeoutException("Connection timed out"),
                AsyncMock(
                    json=lambda: mock_response,
                    raise_for_status=lambda: None,
                    status_code=200
                )
            ]
            
            result = await client._make_request("GET", "/test")
            
            # Should have made 3 calls (2 retries + 1 success)
            assert mock_request.call_count == 3
            assert result == mock_response


@pytest.mark.asyncio 
async def test_retry_logic_with_connection_error():
    """Test that connection errors trigger retries."""
    mock_response = {"id": 1, "shikonaEn": "Test"}
    
    async with SumoClient(max_retries=1, retry_backoff_factor=0.1) as client:
        with patch.object(client._client, "request") as mock_request:
            # First call raises connection error, second succeeds
            mock_request.side_effect = [
                httpx.ConnectError("Connection failed"),
                AsyncMock(
                    json=lambda: mock_response,
                    raise_for_status=lambda: None,
                    status_code=200
                )
            ]
            
            result = await client._make_request("GET", "/test")
            
            assert mock_request.call_count == 2
            assert result == mock_response


@pytest.mark.asyncio
async def test_retry_logic_with_429_status():
    """Test that 429 (Too Many Requests) status triggers retries."""
    mock_response = {"id": 1, "shikonaEn": "Test"}
    
    async with SumoClient(max_retries=1, retry_backoff_factor=0.1) as client:
        with patch.object(client._client, "request") as mock_request:
            # Create a mock 429 response
            mock_429_response = MagicMock()
            mock_429_response.status_code = 429
            
            mock_request.side_effect = [
                httpx.HTTPStatusError(
                    "Too Many Requests", 
                    request=MagicMock(), 
                    response=mock_429_response
                ),
                AsyncMock(
                    json=lambda: mock_response,
                    raise_for_status=lambda: None,
                    status_code=200
                )
            ]
            
            result = await client._make_request("GET", "/test")
            
            assert mock_request.call_count == 2
            assert result == mock_response


@pytest.mark.asyncio
async def test_retry_logic_with_408_status():
    """Test that 408 (Request Timeout) status triggers retries."""
    mock_response = {"id": 1, "shikonaEn": "Test"}
    
    async with SumoClient(max_retries=1, retry_backoff_factor=0.1) as client:
        with patch.object(client._client, "request") as mock_request:
            # Create a mock 408 response
            mock_408_response = MagicMock()
            mock_408_response.status_code = 408
            
            mock_request.side_effect = [
                httpx.HTTPStatusError(
                    "Request Timeout", 
                    request=MagicMock(), 
                    response=mock_408_response
                ),
                AsyncMock(
                    json=lambda: mock_response,
                    raise_for_status=lambda: None,
                    status_code=200
                )
            ]
            
            result = await client._make_request("GET", "/test")
            
            assert mock_request.call_count == 2
            assert result == mock_response


@pytest.mark.asyncio
async def test_no_retry_on_4xx_errors():
    """Test that 4xx errors (except 408, 429) don't trigger retries."""
    async with SumoClient(max_retries=2) as client:
        with patch.object(client._client, "request") as mock_request:
            # Create a mock 400 response
            mock_400_response = MagicMock()
            mock_400_response.status_code = 400
            
            mock_request.side_effect = httpx.HTTPStatusError(
                "Bad Request", 
                request=MagicMock(), 
                response=mock_400_response
            )
            
            with pytest.raises(httpx.HTTPStatusError):
                await client._make_request("GET", "/test")
            
            # Should only make 1 call, no retries
            assert mock_request.call_count == 1


@pytest.mark.asyncio
async def test_exponential_backoff_timing():
    """Test that exponential backoff works correctly."""
    async with SumoClient(max_retries=2, retry_backoff_factor=0.1) as client:
        with patch.object(client._client, "request") as mock_request:
            with patch("asyncio.sleep") as mock_sleep:
                mock_request.side_effect = [
                    httpx.TimeoutException("Timeout"),
                    httpx.TimeoutException("Timeout"),
                    httpx.TimeoutException("Timeout")  # All calls fail
                ]
                
                with pytest.raises(httpx.TimeoutException):
                    await client._make_request("GET", "/test")
                
                # Should have called sleep twice (after 1st and 2nd failures)
                assert mock_sleep.call_count == 2
                
                # Check exponential backoff: 0.1 * (2^0) = 0.1, 0.1 * (2^1) = 0.2
                mock_sleep.assert_any_call(0.1)
                mock_sleep.assert_any_call(0.2)


@pytest.mark.asyncio
async def test_max_retries_exhausted():
    """Test behavior when all retries are exhausted."""
    async with SumoClient(max_retries=1, retry_backoff_factor=0.1) as client:
        with patch.object(client._client, "request") as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Always timeout")
            
            with pytest.raises(httpx.TimeoutException):
                await client._make_request("GET", "/test")
            
            # Should make 2 calls (1 initial + 1 retry)
            assert mock_request.call_count == 2


@pytest.mark.asyncio
async def test_no_retries_when_max_retries_zero():
    """Test that no retries happen when max_retries is 0."""
    async with SumoClient(max_retries=0) as client:
        with patch.object(client._client, "request") as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Timeout")
            
            with pytest.raises(httpx.TimeoutException):
                await client._make_request("GET", "/test")
            
            # Should only make 1 call
            assert mock_request.call_count == 1


@pytest.mark.asyncio
async def test_404_error_handling():
    """Test proper handling of 404 errors with error messages."""
    async with SumoClient() as client:
        with patch.object(client._client, "request") as mock_request:
            mock_404_response = MagicMock()
            mock_404_response.status_code = 404
            mock_404_response.json.return_value = {"error": "Rikishi not found"}
            
            mock_request.return_value = mock_404_response
            
            with pytest.raises(ValueError, match="API Error: Rikishi not found"):
                await client._make_request("GET", "/test")


@pytest.mark.asyncio
async def test_timeout_configuration():
    """Test that timeout configuration is properly applied."""
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        
        client = SumoClient(
            connect_timeout=10.0,
            read_timeout=15.0,
            enable_http2=False,
        )
        
        async with client:
            pass
        
        # Verify AsyncClient was called with correct timeout configuration
        mock_client_class.assert_called_once()
        call_kwargs = mock_client_class.call_args[1]
        
        assert call_kwargs["http2"] is False
        
        timeout = call_kwargs["timeout"]
        assert timeout.connect == 10.0
        assert timeout.read == 15.0
        assert timeout.write == 15.0  # Should use read timeout
        assert timeout.pool == 10.0   # Should use connect timeout


@pytest.mark.asyncio
async def test_ssl_context_with_certifi():
    """Test SSL context creation when certifi is available."""
    with patch("httpx.AsyncClient") as mock_client_class:
        with patch("ssl.create_default_context") as mock_ssl_context:
            with patch("certifi.where", return_value="/path/to/certs"):
                mock_client = AsyncMock()
                mock_client_class.return_value = mock_client
                mock_client.__aenter__.return_value = mock_client
                
                client = SumoClient(verify_ssl=True)
                
                async with client:
                    pass
                
                # Should have created SSL context with certifi
                mock_ssl_context.assert_called_once_with(cafile="/path/to/certs")


@pytest.mark.asyncio
async def test_ssl_context_without_certifi():
    """Test SSL context creation when certifi is not available."""
    with patch("httpx.AsyncClient") as mock_client_class:
        with patch("ssl.create_default_context") as mock_ssl_context:
            with patch("certifi.where", side_effect=ImportError("No certifi")):
                mock_context = MagicMock()
                mock_ssl_context.return_value = mock_context
                
                mock_client = AsyncMock()
                mock_client_class.return_value = mock_client
                mock_client.__aenter__.return_value = mock_client
                
                client = SumoClient(verify_ssl=True)
                
                async with client:
                    pass
                
                # Should have created default SSL context and disabled verification
                mock_ssl_context.assert_called_once_with()
                assert mock_context.check_hostname is False
                assert mock_context.verify_mode == 0  # ssl.CERT_NONE


@pytest.mark.asyncio
async def test_runtime_error_without_context_manager():
    """Test that using client methods without context manager raises RuntimeError."""
    client = SumoClient()
    
    with pytest.raises(RuntimeError, match="Client must be used as an async context manager"):
        await client._make_request("GET", "/test")
