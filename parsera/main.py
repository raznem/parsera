import asyncio
from langchain_core.language_models import BaseChatModel
import enum
from parsera.engine.model import GPT4oMiniModel
from parsera.engine.simple_extractor import TabularExtractor, ListExtractor, ItemExtractor
from parsera.page import fetch_page_content


class Parsera:
    class ExtractorType(enum.Enum):
        LIST = ListExtractor
        TABULAR = TabularExtractor
        ITEM = ItemExtractor

    def __init__(self, model: BaseChatModel | None = None, extractor: ExtractorType = ExtractorType.TABULAR):
        if model is None:
            self.model = GPT4oMiniModel()
        else:
            self.model = model
        self.extractor = extractor

    async def _run(
        self, url: str, elements: dict, proxy_settings: dict | None = None
    ) -> dict:
        if proxy_settings:
            content = await fetch_page_content(url=url, proxy_settings=proxy_settings)
        else:
            content = await fetch_page_content(url=url)
        extractor_instance = self.extractor.value(
            elements=elements, model=self.model, content=content
        )
        result = await extractor_instance.run()
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
