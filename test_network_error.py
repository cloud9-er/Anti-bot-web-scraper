
import urllib.error
from unittest.mock import patch
from response import Response


def test_network_error_propagates():
    network_error = urllib.error.URLError("Simulated connection failure")

    with patch(
        "response.urllib.request.urlopen",
        side_effect=network_error
    ):
        try:
            Response.from_openurllib("https://example.com")
        except urllib.error.URLError:
            print("Network error propagation test passed.")
        else:
            raise AssertionError("Expected URLError to propagate")


if __name__ == "__main__":
    test_network_error_propagates()
