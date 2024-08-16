import asyncio

from langchain_core.language_models import BaseChatModel

from parsera.engine.model import GPT4oMiniModel
from parsera.engine.simple_extractor import TabularExtractor
from parsera.page import fetch_page_content


class Parsera:
    def __init__(self, model: BaseChatModel | None = None):
        if model is None:
            self.model = GPT4oMiniModel()
        else:
            self.model = model

    async def _run(
        self, url: str, elements: dict, proxy_settings: dict | None = None
    ) -> dict:
        if proxy_settings:
            content = await fetch_page_content(url=url, proxy_settings=proxy_settings)
        else:
            content = await fetch_page_content(url=url)
        extractor = TabularExtractor(
            elements=elements, model=self.model, content=content
        )
        result = await extractor.run()
        return result

    def run(self, url: str, elements: dict, proxy_settings: dict | None = None) -> dict:
        return asyncio.run(
            self._run(url=url, elements=elements, proxy_settings=proxy_settings)
        )

    async def arun(
        self, url: str, elements: dict, proxy_settings: dict | None = None
    ) -> dict:
        return await self._run(
            url=url, elements=elements, proxy_settings=proxy_settings
        )
