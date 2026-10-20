
from base import decompose


def test_decompose_url_parts():
    result = decompose(
        "https://books.toscrape.com:8443/catalogue/page-1.html?sort=price#details"
    )

    assert result["scheme"] == "https"
    assert result["host"] == "books.toscrape.com"
    assert result["port"] == 8443
    assert result["path"] == "/catalogue/page-1.html"
    assert result["query"] == "sort=price"
    assert result["fragment"] == "details"

def test_decompose_url_defaults():
    result = decompose("https://example.com")

    assert result["scheme"] == "https"
    assert result["host"] == "example.com"
    assert result["port"] is None
    assert result["path"] == "/"
if __name__ == "__main__":
    test_decompose_url_parts()
    print("URL parsing test passed.")
    test_decompose_url_defaults()
    print("Test for the defaults has passed")