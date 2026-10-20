
from unittest.mock import patch, MagicMock
from response import Response


def test_timeout_is_passed_to_urlopen():
    fake_response = MagicMock()
    fake_response.status = 200
    fake_response.getheaders.return_value = []
    fake_response.reason = "OK"
    fake_response.read.return_value = b"Hello"
    fake_response.headers.get_all.return_value = []

    with patch("response.urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = fake_response

        Response.from_openurllib("https://example.com", timeout=3)

        mock_urlopen.assert_called_once_with(
            "https://example.com",
            timeout=3
        )


if __name__ == "__main__":
    test_timeout_is_passed_to_urlopen()
    print("Timeout test passed.")
