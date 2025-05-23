import os

import pytest
from langchain_openai import AzureChatOpenAI

from parsera import Parsera
from parsera.engine.structured_extractor import (
    ChunksTabularExtractor,
    StructuredExtractor,
)

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


@pytest.mark.asyncio
async def test_smoke():
    scraper = Parsera(model=llm)
    result = await scraper.arun(url=url, elements=elements, proxy_settings=None)

    assert result


@pytest.mark.asyncio
async def test_smoke_api():
    scraper = Parsera()
    result = await scraper.arun(url=url, elements=elements, proxy_settings=None)

    assert result


@pytest.mark.asyncio
async def test_smoke_structured():
    extractor = StructuredExtractor(model=llm)
    scraper = Parsera(extractor=extractor)
    elements_typed = {
        "Title": {
            "type": "string",
            "description": "News title",
        },
        "Points": {
            "type": "integer",
            "description": "Number of points",
        },
        "Comments": {
            "type": "integer",
            "description": "Number of comments",
        },
    }
    result = await scraper.arun(url=url, elements=elements_typed, proxy_settings=None)

    assert result


@pytest.mark.asyncio
async def test_smoke_structured_prompt_only():
    extractor = ChunksTabularExtractor(model=llm)
    scraper = Parsera(extractor=extractor)
    result = await scraper.arun(
        url=url,
        prompt="Get the title, number of points, and number of comments",
    )

    assert result
