# Precision Mode

By default, Parsera works in `fast` mode. In case it's unable to extract some data, you can use `precision` mode instead. This mode minimizes page reduction, allowing the model to detect data hidden inside HTML tags. Keep in mind that `precision` mode uses more [credits](getting-started.md#credits) due to its increased resource requirements. 

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
    "mode": "precision"
}'
```
