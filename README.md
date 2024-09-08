# 📦 Parsera

[![Website](https://img.shields.io/badge/Site-parsera.org-blue?style=for-the-badge)](https://parsera.org)
[![](https://dcbadge.limes.pink/api/server/https://discord.gg/gYXwgQaT7p?compact=true)](https://discord.gg/gYXwgQaT7p)
[![Downloads](https://img.shields.io/pepy/dt/parsera?style=for-the-badge)](https://pepy.tech/project/parsera)

Lightweight Python library for scraping websites with LLMs. 
You can test it on [Parsera website](https://parsera.org).

## Why Parsera?
Because it's simple and lightweight, with minimal token use which boosts speed and reduces expenses.

## Table of Contents
- [Installation](#Installation)
- [Documentation](#Documentation)
- [Basic usage](#Basic-usage)
- [Running with Jupyter Notebook](#Running-with-Jupyter-Notebook)
- [Running as standalone command line tool](#Running-as-standalone-command-line-tool)
- [Running in Docker](#Running-in-Docker)
    - [Prerequisites](#Prerequisites)
    - [Prepare Your Environment](#Prepare-Your-Environment)
    - [Defining scheme for parsing](#Defining-scheme-for-parsing)
    - [Accessing the Output](#Accessing-the-Output)
    - [Make Targets](#Make-Targets)

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

## Running as standalone command line tool

Before you run `Parsera` as CLI tool don't forget to put your `OPENAI_API_KEY` to env variables or `.env` file

### Usage

You can configure elemements to parse using `JSON string` or `FILE`.
Optionally, you can provide `FILE` to write output.

```sh
python -m parsera.main URL {--scheme '{"title":"h1"}' | --file FILENAME} [--output FILENAME]
```

## Running in Docker

You can get access to the CLI or development environment using Docker.

### Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Prepare Your Environment

Create a .env file in the project root directory with the following content:

```env
URL=https://parsera.org
FILE=/app/scheme.json
OUTPUT=/app/output/result.json
```

### Defining scheme for parsing
Parsing scheme should be defined in the file `scheme.json`, which would be mounted as volume to the container to the `/app/scheme.json`

### Accessing the Output
The results will be saved in the output directory on your local machine, which is mapped to `/app/output` inside the container. You can find the output file at `./output/result.json` on your host machine.

### Make Targets

```sh
make build # Build Docker image

make up # Start containers using Docker Compose

make down # Stop and remove containers using Docker Compose

make restart # Restart containers using Docker Compose

make logs # View logs of the containers

make shell # Open a shell in the running container

make clean # Remove all stopped containers, unused networks, and dangling images
```
