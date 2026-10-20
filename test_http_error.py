
from unittest.mock import patch, MagicMock
import urllib.error
from response import Response


def test_http_error_returns_response():
    error_headers = MagicMock()
    error_headers.get_all.return_value = []
    error_headers.items.return_value = [("Content-Type", "text/plain")]

    error = urllib.error.HTTPError(
        url="https://example.com/missing",
        code=404,
        msg="Not Found",
        hdrs=error_headers,
        fp=None,
    )
    error.read = MagicMock(return_value=b"Not found")

    with patch("response.urllib.request.urlopen", side_effect=error):
        result = Response.from_openurllib("https://example.com/missing")

    assert result.status == 404
    assert result.reason == "Not Found"
    assert result.body == "Not found"
    assert result.cookies == []
    print("HTTP error test passed.")


if __name__ == "__main__":
    test_http_error_returns_response()
