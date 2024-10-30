## Different extractor types
There are different types of extractors, that provide output in different formats:

- For tables.
    - `ChunksTabularExtractor` - for tables, capable of processing larger pages with chunking
    - `TabularExtractor` - for tables
- `ListExtractor` for separate lists of values.
- `ItemExtractor` for specific values.

By default a [`ChunksTabularExtractor`](#chunks-tabular-extractor) is used.

## Tabular Extractor
```python
from parsera import Parsera, ExtractorType

scraper = Parsera(extractor=ExtractorType.TABULAR)
```
The tabular extractor is used to find rows of tabular data and has output of the form:
```json
[
    {"name": "name1", "price": "100"},
    {"name": "name2", "price": "150"},
    {"name": "name3", "price": "300"},
]
```

## Chunks Tabular Extractor
Provides the same output format as `TabularExtractor`, but capable of processing larger pages due to page chunking.
For example, if your model has 16k context size, you can set chunks to be not larger than 12k:
```python
from parsera import Parsera, ExtractorType

scraper = Parsera(extractor=ExtractorType.CHUNKS_TABULAR, chunk_size=12000)
```

By default number of tokens is counted based on the OpenAI tokenizer for `gpt-4o` model, but you can provide custom
function for counting tokens:

```python
import tiktoken

def count_tokens(text):
    # Initialize the tokenizer for GPT-4o-mini
    encoding = tiktoken.get_encoding("cl100k_base")

    # Count tokens
    tokens = encoding.encode(text)
    return len(tokens)

scraper = Parsera(extractor=ExtractorType.CHUNKS_TABULAR, chunk_size=12000, token_counter=count_tokens)
```


## List Extractor
```python
from parsera import Parsera, ExtractorType

scraper = Parsera(extractor=ExtractorType.LIST)
```
The list extractor is used to find lists of different values and has output of the form:
```json
{
    "name": ["name1", "name2", "name3"],
    "price": ["100", "150", "300"]
}
```

## Item Extractor
```python
from parsera import Parsera, ExtractorType

scraper = Parsera(extractor=ExtractorType.ITEM)
```
The item extractor is used to get singular items from a page like a title or price and has output of the form:
```json
{
    "name": "name1",
    "price": "100"
}
```
