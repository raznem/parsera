import asyncio
import enum
from typing import Awaitable, Callable

from langchain_core.language_models import BaseChatModel
from playwright.async_api import Page

from parsera.engine.model import GPT4oMiniModel
from parsera.engine.simple_extractor import (
    ItemExtractor,
    ListExtractor,
    TabularExtractor,
)
from parsera.page import PageLoader


class ExtractorType(enum.Enum):
    LIST = ListExtractor
    TABULAR = TabularExtractor
    ITEM = ItemExtractor


class Parsera:
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
        self,
        url: str,
        elements: dict,
        proxy_settings: dict | None = None,
        scrolls_limit: int = 0,
    ) -> dict:
        content = await self.loader.load_content(
            url=url, proxy_settings=proxy_settings, scrolls_limit=scrolls_limit
        )
        extractor_instance = self.extractor.value(
            elements=elements, model=self.model, content=content
        )
        result = await extractor_instance.run()
        return result

    def run(
        self,
        url: str,
        elements: dict,
        proxy_settings: dict | None = None,
        scrolls_limit: int = 0,
    ) -> dict:
        return asyncio.run(
            self._run(
                url=url,
                elements=elements,
                proxy_settings=proxy_settings,
                scrolls_limit=scrolls_limit,
            )
        )

    async def arun(
        self,
        url: str,
        elements: dict,
        proxy_settings: dict | None = None,
        scrolls_limit: int = 0,
    ) -> dict:
        return await self._run(
            url=url,
            elements=elements,
            proxy_settings=proxy_settings,
            scrolls_limit=scrolls_limit,
        )


class ParseraScript(Parsera):
    def __init__(
        self,
        model: BaseChatModel | None = None,
        extractor: ExtractorType = ExtractorType.TABULAR,
        initial_script: Callable[[Page], Awaitable[Page]] | None = None,
        stealth: bool = True,
    ):
        super().__init__(model=model, extractor=extractor)
        self.initial_script = initial_script
        self.stealth = stealth

    async def new_session(
        self,
        proxy_settings: dict | None = None,
        initial_script: Callable[[Page], Awaitable[Page]] | None = None,
        stealth: bool = True,
    ) -> None:
        await self.loader.create_session(
            proxy_settings=proxy_settings,
            playwright_script=initial_script,
            stealth=stealth,
        )

    async def extract_page(
        self,
        url: str,
        elements: dict,
        scrolls_limit: int = 0,
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ):
        content = await self.loader.fetch_page(
            url=url, scrolls_limit=scrolls_limit, playwright_script=playwright_script
        )

        extractor_instance = self.extractor.value(
            elements=elements, model=self.model, content=content
        )
        result = await extractor_instance.run()
        return result

    async def _run(
        self,
        url: str,
        elements: dict,
        scrolls_limit: int = 0,
        proxy_settings: dict | None = None,
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ):
        if self.loader.context is None:
            await self.new_session(
                proxy_settings=proxy_settings,
                initial_script=self.initial_script,
                stealth=self.stealth,
            )
        return await self.extract_page(
            url=url,
            elements=elements,
            scrolls_limit=scrolls_limit,
            playwright_script=playwright_script,
        )

    def run(
        self,
        url: str,
        elements: dict,
        scrolls_limit: int = 0,
        proxy_settings: dict | None = None,
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ) -> dict:
        return asyncio.run(
            self._run(
                url=url,
                elements=elements,
                scrolls_limit=scrolls_limit,
                proxy_settings=proxy_settings,
                playwright_script=playwright_script,
            )
        )

    async def arun(
        self,
        url: str,
        elements: dict,
        scrolls_limit: int = 0,
        proxy_settings: dict | None = None,
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ) -> dict:
        return await self._run(
            url=url,
            elements=elements,
            scrolls_limit=scrolls_limit,
            proxy_settings=proxy_settings,
            playwright_script=playwright_script,
        )
