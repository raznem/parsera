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

## Using proxy
You can use serve the traffic via proxy server when calling `run` method:
```python
proxy_settings = {
    "server": "https://1.2.3.4:5678",
    "username": <PROXY_USERNAME>,
    "password": <PROXY_PASSWORD>,
}
result = scrapper.run(url=url, elements=elements, proxy_settings=proxy_settings)
```

## Run with custom model
You can instantiate `Parsera` with any chat model supported by LangChain, for example, to run the model from Azure:  
```python
import os
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_GPT_BASE_URL"),
    openai_api_version="2023-05-15",
    deployment_name=os.getenv("AZURE_GPT_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_GPT_API_KEY"),
    openai_api_type="azure",
    temperature=0.0,
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

## Run local model with HuggingFace `Trasformers`
Currently, we only support models that include a `system` token

> You should install `Transformers` with either `pytorch` (recommended) or `TensorFlow 2.0`

[Transformers Installation Guide](https://huggingface.co/docs/transformers/en/installation)

example:
```python
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from parsera.engine.model import HuggingFaceModel
from parsera import Parsera

# Define the URL and elements to scrape
url = "https://news.ycombinator.com/"
elements = {
"Title": "News title",
"Points": "Number of points",
"Comments": "Number of comments",
}

# Initialize model with transformers pipeline
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=5000)

# Initialize HuggingFaceModel
llm = HuggingFaceModel(pipeline=pipe)

# Scrapper with HuggingFace model
scrapper = Parsera(model=llm)
result = scrapper.run(url=url, elements=elements)
```

## Using different extractor types
By default a tabular extractor is used, but you can also use the list or item extractors:
```python
from parsera import Parsera

scraper = Parsera(extractor=Parsera.ExtractorType.LIST)
# or
scraper = Parsera(extractor=Parsera.ExtractorType.ITEM)
```

The tabular extractor is used to find rows of tabular data and has output of the form:
```json
[
    {"name": "name1", "price": "100"},
    {"name": "name2", "price": "150"},
    {"name": "name3", "price": "300"},
]
```

The list extractor is used to find lists of different values and has output of the form:
```json
{
    "name": ["name1", "name2", "name3"],
    "price": ["100", "150", "300"]
}
```

The item extractor is used to get singular items from a page like a title or price and has output of the form:
```json
{
    "name": "name1",
    "price": "100"
}
```

## Running with Jupyter Notebook:
Either place this code at the beginning of your notebook:
```python
import nest_asyncio
nest_asyncio.apply()
```

Or instead of calling `run` method use async `arun`.
