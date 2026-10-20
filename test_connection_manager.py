
from unittest.mock import patch,Mock

from base import ConnectionKey, HTTPConnectionManager,get_response


def test_create_uses_expected_connection_settings():
    manager = HTTPConnectionManager(maximum=2, timeout=5.0)
    key = ConnectionKey("example.com", 8443)

    with patch("base.http.client.HTTPSConnection") as mock_connection:
        manager.create(key)

        mock_connection.assert_called_once_with(
            host="example.com",
            port=8443,
            timeout=5.0,
            context=manager._ssl_context,
        )



def test_acquire_creates_and_reuses_connection():
    manager = HTTPConnectionManager(maximum=2)

    with patch.object(manager, "create") as mock_create:
        first = manager.acquire("example.com", 443)
        manager.release(first)
        second = manager.acquire("example.com", 443)

        assert first is second
        mock_create.assert_called_once()


def test_acquire_respects_maximum():
    manager = HTTPConnectionManager(maximum=1)

    with patch.object(manager, "create") as mock_create:
        manager.acquire("example.com", 443)

        try:
            manager.acquire("other.example.com", 443)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Expected maximum connection limit error")

        mock_create.assert_called_once()

def test_shutdown_closes_and_removes_connection():
    manager = HTTPConnectionManager(maximum=2)

    with patch.object(manager, "create") as mock_create:
        conn = manager.acquire("example.com", 443)

        manager.shutdown(conn)

        conn.close.assert_called_once()
        assert conn not in manager._in_use
        assert ("example.com", 443) not in manager._connections

def test_get_response_reuses_connection():
    manager = HTTPConnectionManager(maximum=2)
    conn = Mock()

    first_response = Mock()
    first_response.status = 200
    first_response.reason = "OK"
    first_response.getheaders.return_value = [
        ("Content-Type", "text/plain")
    ]
    first_response.read.return_value = b"first response"

    second_response = Mock()
    second_response.status = 200
    second_response.reason = "OK"
    second_response.getheaders.return_value = [
        ("Content-Type", "text/plain")
    ]
    second_response.read.return_value = b"second response"

    conn.getresponse.side_effect = [
        first_response,
        second_response,
    ]

    with patch.object(manager, "create", return_value=conn) as mock_create:
        first = get_response("https://example.com/first", manager)
        second = get_response("https://example.com/second", manager)

        assert first["status"] == 200
        assert first["body"] == "first response"
        assert second["status"] == 200
        assert second["body"] == "second response"

        assert mock_create.call_count == 1
        assert conn.request.call_count == 2
        assert manager._in_use == set()

    print("HTTP request reuse test passed.")

def test_get_response_shuts_down_connection_on_failure():
    manager = HTTPConnectionManager(maximum=2)
    conn = Mock()
    conn.request.side_effect = OSError("Simulated network failure")

    with patch.object(manager, "create", return_value=conn):
        try:
            get_response("https://example.com/", manager)
        except OSError as error:
            assert str(error) == "Simulated network failure"
        else:
            raise AssertionError("Expected network error")

    conn.close.assert_called_once()
    assert manager._in_use == set()
    assert ("example.com", 443) not in manager._connections

    print("Failed-request cleanup test passed.")


if __name__ == "__main__":
    test_create_uses_expected_connection_settings()
    print("Connection creation test passed.")
    test_acquire_creates_and_reuses_connection()
    test_acquire_respects_maximum()
    print("Acquire and reuse tests passed.")
    test_shutdown_closes_and_removes_connection()
    print("Shutdown test passed.")