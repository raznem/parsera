import asyncio
import enum

from langchain_core.language_models import BaseChatModel

from parsera.engine.model import GPT4oMiniModel
from parsera.engine.simple_extractor import (
    ItemExtractor,
    ListExtractor,
    TabularExtractor,
)
from parsera.page import PageLoader, fetch_page_content


class Parsera:
    class ExtractorType(enum.Enum):
        LIST = ListExtractor
        TABULAR = TabularExtractor
        ITEM = ItemExtractor

    def __init__(
        self,
        model: BaseChatModel | None = None,
        extractor: ExtractorType = ExtractorType.TABULAR,
    ):
        if model is None:
            self.model = GPT4oMiniModel()
        else:
            self.model = model
        self.extractor = extractor
        self.loader = PageLoader()

    async def _run(
        self, url: str, elements: dict, proxy_settings: dict | None = None
    ) -> dict:
        content = await self.loader.load_content(url=url, proxy_settings=proxy_settings)
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
