import time
from unittest.mock import MagicMock, patch

import pytest

from crewai_book.exceptions.domain import APIConnectionError, RateLimitExceededError
from crewai_book.shared.gatekeeper import ApiGatekeeper


@pytest.fixture
def mock_config() -> None:
    """Test docstring."""
    with patch("crewai_book.shared.gatekeeper.config_manager") as mock_mgr:
        mock_mgr.get_rate_limits.return_value = {
            "limits": {
                "test_service": {
                    "requests_per_minute": 2,
                    "retry_after_seconds": 0.1,
                    "max_retries": 1,
                }
            }
        }
        yield mock_mgr


def test_gatekeeper_initialization(mock_config) -> None:
    """Test docstring."""
    gk = ApiGatekeeper("test_service")
    assert gk.rpm == 2
    assert gk.retry_after == 0.1
    assert gk.max_retries == 1


def test_gatekeeper_execution_success(mock_config) -> None:
    """Test docstring."""
    gk = ApiGatekeeper("test_service")
    mock_func = MagicMock(return_value="success")
    result = gk.execute(mock_func, "arg1", kwarg1="test")

    assert result == "success"
    mock_func.assert_called_once_with("arg1", kwarg1="test")
    status = gk.get_queue_status()
    assert status["current_size"] == 0


def test_gatekeeper_rate_limiting(mock_config) -> None:
    """Test docstring."""
    gk = ApiGatekeeper("test_service")
    mock_func = MagicMock(return_value="success")

    # Should execute 2 calls immediately
    start_time = time.time()
    gk.execute(mock_func)
    gk.execute(mock_func)
    elapsed = time.time() - start_time
    assert elapsed < 1.0  # Should be fast

    # Third call should hit the rate limit sleep
    # But since sleep_time is 60s we'll mock sleep
    with patch("time.sleep") as mock_sleep:
        gk.execute(mock_func)
        mock_sleep.assert_called_once()


def test_gatekeeper_queue_full(mock_config) -> None:
    """Test docstring."""
    gk = ApiGatekeeper("test_service", max_queue_size=1)
    # Fill the queue manually
    gk.request_queue.put(1)

    mock_func = MagicMock()
    with pytest.raises(RateLimitExceededError):
        gk.execute(mock_func)


def test_gatekeeper_retry_logic(mock_config) -> None:
    """Test docstring."""
    gk = ApiGatekeeper("test_service")

    # Function fails first time, succeeds second
    mock_func = MagicMock(side_effect=[Exception("Transient error"), "success"])

    with patch("time.sleep") as mock_sleep:
        result = gk.execute(mock_func)
        assert result == "success"
        assert mock_func.call_count == 2
        mock_sleep.assert_called_once_with(0.1)


def test_gatekeeper_max_retries_exceeded(mock_config) -> None:
    """Test docstring."""
    gk = ApiGatekeeper("test_service")

    # Function always fails
    mock_func = MagicMock(side_effect=Exception("Permanent error"))

    with patch("time.sleep"):
        with pytest.raises(APIConnectionError, match="Failed after 1 retries"):
            gk.execute(mock_func)
