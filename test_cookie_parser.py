from response import Response

cookie = "session=abc123; Path=/; Secure; SameSite=Lax"
result = Response.cookie_parser(cookie)

print("Parsed cookie:", result)

assert result["name"] == "session"
assert result["value"] == "abc123"
assert result.get("path") == "/"
assert result.get("secure") is True
assert result.get("samesite") == "Lax"

print("All cookie parser checks passed.")
