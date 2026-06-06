from unittest.mock import patch

from crewai_book.observability.logger import get_logger, setup_logger


@patch("crewai_book.observability.logger.logger")
@patch("crewai_book.observability.logger.settings")
def test_setup_logger(mock_settings, mock_logger):
    mock_settings.app_env = "development"
    setup_logger()

    mock_logger.remove.assert_called_once()
    assert mock_logger.add.call_count == 2  # Console and File logger

@patch("crewai_book.observability.logger.logger")
def test_get_logger(mock_logger):
    bound_logger = get_logger("test_module")
    mock_logger.bind.assert_called_once_with(module="test_module")
