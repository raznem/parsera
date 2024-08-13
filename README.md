# Parsera
Lightweight library for scraping web-sites with LLMs. 
You can test it on [Parsera website](https://parsera.org).

## Why Parsera?
Because it's simple and lightweight, with minimal token use it boosts speed and reduces expenses.

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

Next you can run a basic version that uses `gpt-4o-mini`
```python
from parsera import Parsera

url = "https://news.ycombinator.com/"
elements = {
    "Title": "News title",
    "Points": "Number of points",
    "Comments": "Number of comments",
}

scrapper = Parsera()
result = scrapper.run(url=url, elements=elements)
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

## Run with local model
Install Ollama
```shell
pip install langchain-ollama
```

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3",
    temperature=0,
    # other params...
)

url = "https://news.ycombinator.com/"
elements = {
    "Title": "News title",
    "Points": "Number of points",
    "Comments": "Number of comments",
}
scrapper = Parsera(model=llm)
result = scrapper.run(url=url, elements=elements)
```

