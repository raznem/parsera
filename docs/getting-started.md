# Welcome to Parsera

Parsera is a lightweight Python library for scraping websites with LLMs.  
You can clone and run it locally or [use an API](api/getting-started.md), which provides more scalable way and some extra features like built-in proxy.

## Installation

```shell
pip install parsera
playwright install
```

## Basic usage

If you want to use OpenAI, remember to set up `OPENAI_API_KEY` env variable.
You can do this from python with:
```python
import os

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY_HERE"
```

Next, you can run a basic version that uses `gpt-4o-mini`
```python
from parsera import Parsera

url = "https://news.ycombinator.com/"
elements = {
    "Title": "News title",
    "Points": "Number of points",
    "Comments": "Number of comments",
}

scraper = Parsera()
result = scraper.run(url=url, elements=elements)
```

`result` variable will contain a json with a list of records:
```json
[
   {
      "Title":"Hacking the largest airline and hotel rewards platform (2023)",
      "Points":"104",
      "Comments":"24"
   },
    ...
]
```

There is also `arun` async method available:
```python
result = await scrapper.arun(url=url, elements=elements)
```

## Running with CLI

Before you run `Parsera` as command line tool don't forget to put your `OPENAI_API_KEY` to env variables or `.env` file

### Usage

You can configure elements to parse using `JSON string` or `FILE`.
Optionally, you can provide `FILE` to write output.

```sh
python -m parsera.main URL {--scheme '{"title":"h1"}' | --file FILENAME} [--output FILENAME]
```

## More features

Check out further documentation to explore more features:

- [Running custom models](features/custom-models.md)
- [Using proxy](features/proxy.md)
- [Run custom playwright](features/custom-playwright.md)
- [Extractors](features/extractors.md)
- [Docker](features/docker.md)
