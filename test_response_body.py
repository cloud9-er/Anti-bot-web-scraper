
from unittest.mock import patch, MagicMock
from response import Response


def test_invalid_utf8_body_uses_replacement_character():
    fake_response = MagicMock()
    fake_response.status = 200
    fake_response.getheaders.return_value = []
    fake_response.reason = "OK"
    fake_response.read.return_value = b"\xff"
    fake_response.headers.get_all.return_value = []

    with patch("response.urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value = fake_response

        result = Response.from_openurllib("https://example.com")

    assert result.body == "\ufffd"
    print("Invalid UTF-8 fallback test passed.")


if __name__ == "__main__":
    test_invalid_utf8_body_uses_replacement_character()
