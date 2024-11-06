# Precision Mode

If regular Parsera mode is missing specific data, you can enable `precision_mode`. This mode minimizes page reduction, allowing the model to detect data hidden inside HTML tags. Keep in mind that `precision_mode` uses more credits due to its increased resource requirements.

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
    "precision_mode": true
}'
```
