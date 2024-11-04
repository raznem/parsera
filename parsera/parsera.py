import asyncio
from typing import Awaitable, Callable

from langchain_core.language_models import BaseChatModel
from playwright.async_api import Page

from parsera.engine.chunks_extractor import ChunksTabularExtractor
from parsera.engine.model import GPT4oMiniModel
from parsera.engine.simple_extractor import Extractor
from parsera.page import PageLoader


class Parsera:
    def __init__(
        self,
        model: BaseChatModel | None = None,
        extractor: Extractor | None = None,
        initial_script: Callable[[Page], Awaitable[Page]] | None = None,
        stealth: bool = True,
        custom_cookies: list[dict] | None = None,
    ):
        """Initialize Parsera

        Args:
            model (BaseChatModel | None, optional): LangChain Chat Model. Defaults to None which
                invokes usage of GPT4oMiniModel.
            extractor (ExtractorType, optional): Extractor type from the ExtractorType enum.
                Defaults to ExtractorType.TABULAR.
            initial_script (Callable[[Page], Awaitable[Page]] | None, optional): Playwright script
                to execute before the extraction. Defaults to None.
            stealth (bool, optional): Whether to use stealth mode. Defaults to True.
            custom_cookies (list[dict] | None, optional): List of custom cookies to be added to the
                browser context. Defaults to None.
        """
        if model is None:
            self.model = GPT4oMiniModel()
        else:
            self.model = model

        if extractor is None:
            self.extractor = ChunksTabularExtractor(model=self.model)
        else:
            self.extractor = extractor
        self.initial_script = initial_script
        self.stealth = stealth
        self.loader = PageLoader(custom_cookies=custom_cookies)

    async def _run(
        self,
        url: str,
        elements: dict,
        proxy_settings: dict | None = None,
        scrolls_limit: int = 0,
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ) -> dict:
        if self.loader.context is None:
            await self.loader.create_session(
                proxy_settings=proxy_settings,
                playwright_script=self.initial_script,
                stealth=self.stealth,
            )

        content = await self.loader.fetch_page(
            url=url, scrolls_limit=scrolls_limit, playwright_script=playwright_script
        )

        result = await self.extractor.run(content=content, attributes=elements)
        return result

    def run(
        self,
        url: str,
        elements: dict,
        proxy_settings: dict | None = None,
        scrolls_limit: int = 0,
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
        proxy_settings: dict | None = None,
        scrolls_limit: int = 0,
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ) -> dict:
        return await self._run(
            url=url,
            elements=elements,
            scrolls_limit=scrolls_limit,
            proxy_settings=proxy_settings,
            playwright_script=playwright_script,
        )
