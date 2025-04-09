# Getting started

First, find the API key on the `API` tab of the [Parsera web page](https://parsera.org/app).     
Use it as the value of `X-API-KEY` header to authenticate your requests.

## Agents
Agent that generates reusable custom scrapers which has 2 main steps:

1. Call `generate` to build scraper;  
2. Call `scrape` to run this scraper on a specific URL.

### `generate`
Request agent to build a new scraper:
```bash
curl https://agents.parsera.org/v1/generate \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "name": "hackernews",
    "url": "https://news.ycombinator.com/",
    "attributes": {
        "title": "News title",
        "points": "Number of points"
    }
}'
```

**Parameters:**

| Parameter      | Type     | Default     | Description                                |
|----------------|----------|--------------|--------------------------------------------|
| `name`         | `string` | -            | Name of the agent                           |
| `url`          | `string` | -            | Website URL                                |
| `attributes`   | `object`  | -            | A map of `name` - `description` pairs of data fields to extract from the webpage |
| `proxy_country` | `string` | `UnitedStates` | Proxy country, see [Proxy Countries](proxy.md)    |
| `cookies`      | `array`  | Empty        | Cookies to use during extraction, see [Cookies](cookies.md) |

### `scrape`
Use an existing scraper on the webpage:
```bash
curl https://agents.parsera.org/v1/scrape \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "name": "hackernews",
    "url": "https://news.ycombinator.com/front?day=2024-09-11",
}'
```
**Parameters:**

| Parameter      | Type     | Default      | Description                                                              |
|----------------|----------|--------------|--------------------------------------------------------------------------|
| `name`         | `string` | -            | Name of the agent                                                        |
| `url`          | `string` | -            | URL of the webpage to extract data from                                  |
| `proxy_country`| `string` | `UnitedStates`| Proxy country, see [Proxy Countries](proxy.md)                          |
| `cookies`      | `array`  | Empty        | Cookies to use during extraction, see [Cookies](cookies.md)              |


### `list`
List all available agents:
```bash
curl --location 'https://agents.parsera.org/v1/list' \
--header 'X-API-KEY: <YOUR_API_KEY>'
```

### `remove`
Remove existing agent:
```bash
curl --location --request DELETE 'https://agents.parsera.org/v1/remove' \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "name": "hackernews"
}'
```
**Parameters:**

| Parameter      | Type     | Default      | Description                                                              |
|----------------|----------|--------------|--------------------------------------------------------------------------|
| `name`         | `string` | -            | Name of the agent                                                        |


## Extractor
LLM-Powered data extractor is ideal for one-time data extraction and unstructured data.

### `extract`

Paste your API key to the `X-API-KEY` header to send the request to the `extract` endpoint:
```bash
curl https://api.parsera.org/v1/extract \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "url": "https://news.ycombinator.com/",
    "attributes": {
        "title": "News title",
        "points": "Number of points"
    },
    "proxy_country": "Germany"
}'
```

If some data is missing, you can retry with `precision` mode, which looks into data hidden in HTML tags. For details, see [Precision mode](precision-mode.md).

It's recommended to set the `proxy_country` parameter to a specific country since a page could be unavailable from some locations.

**Parameters:**

| Parameter      | Type     | Default      | Description                                      |
|----------------|----------|--------------|--------------------------------------------------|
| `url`          | `string` | -            | URL of the webpage to extract data from          |
| `attributes`   | `object`  | -            | A map of `name` - `description` pairs of data fields to extract from the webpage |
| `mode`         | `string` | `standard`    | Mode of the extractor, `standard` or `precision`. For details, see [Precision mode](precision-mode.md) |
| `proxy_country`| `string` | `UnitedStates`| Proxy country, see [Proxy Countries](proxy.md)    |
| `cookies`      | `array`  | Empty        | Cookies to use during extraction, see [Cookies](cookies.md) |

### `parse`

In addition to `extract`, there is a `parse` endpoint that can be used to parse data generated on your side instead of one from url.  
There is a `content` attribute for passing data, which accepts both raw HTML and string:  
```bash
curl https://api.parsera.org/v1/parse \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "content": <HTML_OR_TEXT_HERE>,
    "attributes": {
        "title": "News title",
        "points": "Number of points"
    }
}'
```

**Parameters:**

| Parameter      | Type     | Default      | Description                                      |
|----------------|----------|--------------|--------------------------------------------------|
| `content`          | `string` | -        | Raw HTML or text content to extract data from |
| `attributes`   | `object`  | -            | A map of `name` - `description` pairs of data fields to extract from the webpage |
| `mode`         | `string` | `standard`    | Mode of the extractor, `standard` or `precision`. For details, see [Precision mode](precision-mode.md) |


### `extract_markdown`

You can get a markdown from URL with the `extract_markdown` endpoint:

```bash
curl https://api.parsera.org/v1/extract_markdown \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "url": "https://news.ycombinator.com/",
    "proxy_country": "UnitedStates"
}'
```

**Parameters:**

| Parameter      | Type     | Default      | Description                                      |
|----------------|----------|--------------|--------------------------------------------------|
| `url`          | `string` | -            | URL of the webpage to extract data from          |
| `proxy_country`| `string` | `UnitedStates`| Proxy country, see [Proxy Countries](proxy.md)    |
| `cookies`      | `array`  | Empty        | Cookies to use during extraction, see [Cookies](cookies.md) |

### Credits
- `standard` mode (Default) - **1 Extract** per call
- `precision` mode - **10 Extracts** per call


### Swagger doc

You can also explore the Swagger doc of the Extractor API: [https://api.parsera.org/docs#/](https://api.parsera.org/docs#/).

## More features

Check out further documentation to explore more features:

- [Setting proxy](proxy.md)
- [Setting cookies](cookies.md)
- [Precision mode](precision-mode.md)
