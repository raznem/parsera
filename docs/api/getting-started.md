# Getting started

First, go to [Parsera web page](https://parsera.org/app) and generate an API key.

Paste this key to `X-API-KEY` header to send the request:
```bash
curl https://api.parsera.org/v1/extract \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "url": "https://news.ycombinator.com/",
    "attributes": [
        {
            "name": "Title",
            "description": "News title"
        },
        {
            "name": "Points",
            "description": "Number of points"
        }
    ],
    "proxy_country": "UnitedStates"
}'
```

By default, `proxy_country` is random, it's recommended to set `proxy_country` parameter to a specific country in the request since a page could not be available from all locations.  
[Here](proxy.md) you can find a full list of proxy countries available.
