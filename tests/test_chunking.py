import os

import pytest
from langchain_openai import AzureChatOpenAI

from parsera import Parsera
from parsera.engine.chunks_extractor import ChunksTabularExtractor

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_GPT_BASE_URL"),
    openai_api_version="2023-05-15",
    deployment_name=os.getenv("AZURE_GPT_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_GPT_API_KEY"),
    openai_api_type="azure",
    temperature=0.0,
)


def values_to_strings(dicts_list: list[dict]):
    for i in range(len(dicts_list)):
        for k, v in dicts_list[i].items():
            dicts_list[i][k] = str(v)
    return dicts_list


async def run_chunks_and_no_chunks(url: str, elements: dict, small_chunk_size: int):
    extractor = ChunksTabularExtractor(model=llm, chunk_size=100000)
    scraper_long_chunk = Parsera(extractor=extractor)
    result_no_chunks = await scraper_long_chunk.arun(
        url=url, elements=elements, proxy_settings=None
    )

    extractor_small_chunk = ChunksTabularExtractor(
        model=llm, chunk_size=small_chunk_size
    )
    scraper_small_chunk = Parsera(extractor=extractor_small_chunk)
    result_chunks = await scraper_small_chunk.arun(
        url=url, elements=elements, proxy_settings=None
    )
    result_no_chunks = values_to_strings(result_no_chunks)
    result_chunks = values_to_strings(result_chunks)
    return result_no_chunks, result_chunks


@pytest.mark.asyncio
async def test_chunking_hackernews():
    url = "https://news.ycombinator.com/front?day=2024-09-05"
    elements = {
        "Title": "News title",
        "Points": "Number of points (only number)",
        "Comments": "Number of comments (only number)",
    }
    result_no_chunks, result_chunks = await run_chunks_and_no_chunks(
        url, elements, small_chunk_size=1500
    )
    assert result_no_chunks == result_chunks


@pytest.mark.asyncio
async def test_chunking_egen_ai():
    url = "https://egen.ai/people/careers/"
    elements = {
        "Title": "Title of job",
        "Location": "Location of job",
        "Type": "If the job is Remote or Not-Remote",
        "Link": "Link to the post",
    }
    result_no_chunks, result_chunks = await run_chunks_and_no_chunks(
        url, elements, small_chunk_size=1500
    )
    assert result_no_chunks != result_chunks
