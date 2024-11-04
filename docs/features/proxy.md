## Using proxy
You can use serve the traffic via proxy server when calling `run` method:
```python
from parsera import Parsera

scraper = Parsera()
proxy_settings = {
    "server": "https://1.2.3.4:5678",
    "username": <PROXY_USERNAME>,
    "password": <PROXY_PASSWORD>,
}
result = scraper.run(url=url, elements=elements, proxy_settings=proxy_settings)
```

Where `proxy_settings` contains your proxy credentials.