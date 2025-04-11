# Output Types

API allows you to specify output types via alternative schema of `attributes` in all endpoints. 

## New Schema
Simply replace old attributes values:
```json
"attributes": {
    "title": "News title",
    "points": "Number of points"
}
```

With alternative schema that includes specific data types:

```json
"attributes": {
    "title": {
        "description": "Title of the article",
        "type": "string"
    },
    "points": {
        "description": "Number of points",
        "type": "integer"
    },
}
```

## Data Types
You can use one of the following data types:

| Type value | Output | Example |
|------|-------------|---------|
| `any` | Model can return any type (default) | - |
| `string` | Text value | `Hello World` |
| `integer` | Integer number | `1` |
| `number` | Floating point number | `1.23` |
| `bool` | Boolean value (`true` or `false`) | `true` |
| `list` | List of values | `["hello", "world"]` |
| `object` | Nested structure with map of keys and values. | `{ name: "John Doe" }` |

## Example
Full request example for extract:
```bash
curl https://agents.parsera.org/v1/generate \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "url": "https://news.ycombinator.com/",
    "attributes": {
        "title": {
            "description": "Title of the article",
            "type": "string"
        },
        "points": {
            "description": "Number of points",
            "type": "integer"
        }
    }
}'
```
