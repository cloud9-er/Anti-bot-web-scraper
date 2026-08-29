import urllib.request
from urllib.parse import urlsplit
import http.client
import urllib.error

url="https://books.toscrape.com"

#decomposing URL and obtaining host
decomposed = urlsplit(url)
host = decomposed.netloc

#establishing a connection via http.client
connection = http.client.HTTPSConnection(host,port=443)
#headers = {"Accept": "application/json"}
#req = urllib.request(url, headers = headers)

try:
    with urllib.request.urlopen(url) as response:
        #obtaining headers of the Response
        headers = response.getheaders()
        header = dict(headers)
        #reading data from opened URL
        content = response.read().decode("utf-8")
        print(header)
        print(content[:200])
except urllib.error.HTTPError as e:
    print(e.status)
finally:
    connection.close()