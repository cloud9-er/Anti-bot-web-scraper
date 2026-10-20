from response import Response

for name, url in {
    "technology": "https://www.bbc.com/news/technology",
    "business": "https://www.bbc.com/news/business",
    "world": "https://www.bbc.com/news/world",
}.items():
    r = Response.from_openurllib(url, timeout=10)
    print(name, "->", r.status)