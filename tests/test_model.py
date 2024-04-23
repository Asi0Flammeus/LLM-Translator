import pytest
from unittest.mock import patch, Mock

from model import *

@pytest.mark.parametrize("error, expected_error_message", [
    (RateLimitError, "Rate limit"),
    (Timeout, "Timeout"),
    (APIError, "API"),
    (ServiceUnavailableError, "Service Unavailable"),
    (Exception, "Unknown")
])


def test_handle_error(error, expected_error_message):
    handler = APIErrorHandler()

    with patch("builtins.print") as mock_print, patch("time.sleep") as mock_sleep:
        handler.handle_error(error("Unknown"))

        mock_print.assert_called_with(f"An {expected_error_message} error occured. Retry in {handler.sleep_time} seconds...")

        mock_sleep.assert_called_with(handler.sleep_time)
