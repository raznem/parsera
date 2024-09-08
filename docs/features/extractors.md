## Different extractor types
There are different types of extractors, that provide output in different formats:

- `TabularExtractor` for tables.
- `ListExtractor` for separate lists of values.
- `ItemExtractor` for specific values.

By default a tabular extractor is used.

## Tabular extractor
```python
from parsera import Parsera

scraper = Parsera(extractor=Parsera.ExtractorType.TABULAR)
```
The tabular extractor is used to find rows of tabular data and has output of the form:
```json
[
    {"name": "name1", "price": "100"},
    {"name": "name2", "price": "150"},
    {"name": "name3", "price": "300"},
]
```

## List extractor
```python
from parsera import Parsera

scraper = Parsera(extractor=Parsera.ExtractorType.LIST)
```
The list extractor is used to find lists of different values and has output of the form:
```json
{
    "name": ["name1", "name2", "name3"],
    "price": ["100", "150", "300"]
}
```

## Item extractor
```python
from parsera import Parsera

scraper = Parsera(extractor=Parsera.ExtractorType.ITEM)
```
The item extractor is used to get singular items from a page like a title or price and has output of the form:
```json
{
    "name": "name1",
    "price": "100"
}
```
