# Getting started

First, go to [Parsera web page](https://parsera.org/app) and generate an API key.

## Extract endpoint

Paste this key to `X-API-KEY` header to send the request to `extract` endpoint:
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

If some data is missing, you can retry with `precision` mode, which does lighter page reduction and can find data hidden in HTML tags. For details, see [Precision mode](precision-mode.md).

By default, `proxy_country` is `UnitedStates`, it's recommended to set `proxy_country` parameter to a specific country in the request since a page could not be available from all locations. [Here](proxy.md) you can find a full list of proxy countries available.

## Parse endpoint

In addition to `extract`, there is a `parse` endpoint that can be used to parse data generated on your side instead of one from url.  
There is a `content` attribute for passing data, which accepts both raw html and string:  
```bash
curl https://api.parsera.org/v1/parse \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "content": <HTML_OR_TEXT_HERE>,
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
}'
```

## Credits
- `fast` mode (Default) - **1 credit** per call
- `precision` mode - **10 credits** per call


## Swagger doc

You can also explore Swagger doc of the API following this link: [https://api.parsera.org/docs#/](https://api.parsera.org/docs#/).

## More features

Check out further documentation to explore more features:

- [Setting proxy](proxy.md)
- [Setting cookies](cookies.md)
- [Precision mode](precision-mode.md)
