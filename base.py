import urllib.request
from urllib.parse import urlsplit
import http.client
import urllib.error

import ssl

url = "https://books.toscrape.com"

class URL():
    def __init__(self, scheme, netloc, path = None, query = None, fragment = None):
        self.scheme = scheme
        self.netloc = netloc
        self.path = path
        self.query = query
        self.fragment = fragment

class ConnectionKey():
    def __init__(self, host, port):
        self.host = host
        self.port = port

class HTTPConnectionManager():
    def __init__(self, maximum = 2, timeout = 5.0):
        self.maximum = maximum
        self.timeout = timeout
        self._connections = {}
        self._in_use = set()

        self._ssl_context = ssl.create_default_context()

    def create(self, key):
        return http.client.HTTPSConnection(host = key.host, port = key.port, timeout = self.timeout, context = self._ssl_context)

    def acquire(self, host, port = 443):
        key = (host, port)
        connections = self._connections.get(key, [])

        for conn in connections:
            if conn not in self._in_use:
                self._in_use.add(conn)
                return conn

        total_connections = sum(
            len(group) for group in self._connections.values()
    )

        if total_connections >= self.maximum:
            raise RuntimeError("Maximum connection limit reached")

        connection_key = ConnectionKey(host, port)
        conn = self.create(connection_key)

        self._connections.setdefault(key, []).append(conn)
        self._in_use.add(conn)
        return conn
    def release(self, conn):
        if conn not in self._in_use:
            raise ValueError("Connection is not currently in use")
        self._in_use.remove(conn)

    def shutdown(self, conn):
        for key, connections in list(self._connections.items()):
            if conn in connections:
                connections.remove(conn)
                if not connections:
                    del self._connections[key]
                self._in_use.discard(conn)
                conn.close()
                return
        raise ValueError("Connection is not managed by this manager")

def decompose(url):
    decomposed = urlsplit(url)
    decomposed_dict = {
        "scheme" : decomposed.scheme,
        "host" : decomposed.hostname,
        "port": decomposed.port,
        "path" : decomposed.path or '/',
        "query" : decomposed.query,
        "fragment" : decomposed.fragment
    }
    return decomposed_dict

def connect(host, port = 443):
    return http.client.HTTPSConnection(host, port)

def get_response(url, manager):
    parts = decompose(url)

    if parts["scheme"] != "https":
        raise ValueError("Only HTTPS URLs are supported")

    host = parts["host"]
    port = parts["port"] or 443
    path = parts["path"]

    if parts["query"]:
        path += "?" + parts["query"]

    conn = manager.acquire(host, port)

    try:
        conn.request("GET", path)
        response = conn.getresponse()

        headers = response.getheaders()
        body = response.read().decode("utf-8", errors="replace")

        result = {
            "status": response.status,
            "reason": response.reason,
            "headers": headers,
            "body": body,
        }
    except Exception:
        manager.shutdown(conn)
        raise
    else:
        manager.release(conn)
        return result



if __name__ == "__main__":
    manager = HTTPConnectionManager()
    try:
        response = get_response(url, manager)
        print("Status:", response["status"])
        print("Reason:", response["reason"])
        print("Body preview:", response["body"][:300])
    finally:
        for connections in list(manager._connections.values()):
            for conn in list(connections):
                manager.shutdown(conn)
