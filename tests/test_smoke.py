import os

import pytest
from langchain_openai import AzureChatOpenAI

from parsera import Parsera

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_GPT_BASE_URL"),
    openai_api_version="2023-05-15",
    deployment_name=os.getenv("AZURE_GPT_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_GPT_API_KEY"),
    openai_api_type="azure",
    temperature=0.0,
)


@pytest.mark.asyncio
async def test_smoke():
    url = "https://news.ycombinator.com/"
    elements = {
        "Title": "News title",
        "Points": "Number of points",
        "Comments": "Number of comments",
    }

    scraper = Parsera(model=llm)
    result = await scraper.arun(url=url, elements=elements, proxy_settings=None)

    assert result
