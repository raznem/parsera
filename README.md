# 📦 Parsera

[![Website](https://img.shields.io/badge/Site-parsera.org-blue?style=for-the-badge)](https://parsera.org)
[![](https://dcbadge.limes.pink/api/server/https://discord.gg/gYXwgQaT7p?compact=true)](https://discord.gg/gYXwgQaT7p)
[![Downloads](https://img.shields.io/pepy/dt/parsera?style=for-the-badge)](https://pepy.tech/project/parsera)

Lightweight Python library for scraping websites with LLMs. 
You can test it on [Parsera website](https://parsera.org).

## Why Parsera?
Because it's simple and lightweight, with minimal token use which boosts speed and reduces expenses.

## Installation

```shell
pip install parsera
playwright install
```

## Documentation

Check out [documentation](https://docs.parsera.org) to learn more about other features, like running custom models and playwright scripts.

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

## Running with Jupyter Notebook:
Either place this code at the beginning of your notebook:
```python
import nest_asyncio
nest_asyncio.apply()
```

Or instead of calling `run` method use async `arun`.
