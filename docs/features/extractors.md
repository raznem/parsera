## Different extractor types
There are different types of extractors, that provide output in different formats:

- For tables.
    - `ChunksTabularExtractor` - for tables, capable of processing larger pages with chunking
    - `TabularExtractor` - for tables, without chunking (fails when page doesn't fit into the model's context)
- `ListExtractor` for separate lists of values.
- `ItemExtractor` for specific values.

By default a [`ChunksTabularExtractor`](#chunks-tabular-extractor) is used.

## Tabular Extractor
```python
from parsera import Parsera
from parsera.engine.simple_extractor import TabularExtractor

extractor = TabularExtractor()
scraper = Parsera(extractor=extractor)
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
For example, if your model has 16k context size, you can set chunks to be not larger than 12k (keeping 4k buffer for other parts of the prompt):
```python
from parsera import Parsera
from parsera.engine.chunks_extractor import ChunksTabularExtractor

extractor = ChunksTabularExtractor(chunk_size=12000)
scraper = Parsera(extractor=extractor)
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

## Structured Extractor
Extension of `ChunksTabularExtractor`, which uses structured output to get the output of specified type:
```python
from parsera import Parsera
from parsera.engine.chunks_extractor import ChunksTabularExtractor

url = "https://news.ycombinator.com/"
elements = {
    "Title": {
        "description": "News title",
        "type": "string",
    },
    "Points": {
        "description": "Number of points",
        "type": "integer",
    }
    "Comments": {
        "description": "Number of comments",
        "type": "integer",
    }
}

extractor = StructuredExtractor()
scraper = Parsera(extractor=extractor)  # With elements input structured as above, will be used by default.

result = scraper.run(url=url, elements=elements)
```

Note: use this extractor only with models supporting Structured Outputs.


## List Extractor
```python
from parsera import Parsera
from parsera.engine.simple_extractor import ListExtractor

extractor = ListExtractor()
scraper = Parsera(extractor=extractor)
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
from parsera import Parsera
from parsera.engine.simple_extractor import ItemExtractor

extractor = ItemExtractor()
scraper = Parsera(extractor=extractor)
```
The item extractor is used to get singular items from a page like a title or price and has output of the form:
```json
{
    "name": "name1",
    "price": "100"
}
```
