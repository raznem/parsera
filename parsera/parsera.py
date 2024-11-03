import asyncio
import enum
from typing import Awaitable, Callable

import tiktoken
from langchain_core.language_models import BaseChatModel
from playwright.async_api import Page

from parsera.engine.chunks_extractor import ChunksTabularExtractor
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
    CHUNKS_TABULAR = ChunksTabularExtractor


class Parsera:
    def __init__(
        self,
        model: BaseChatModel | None = None,
        extractor: ExtractorType = ExtractorType.CHUNKS_TABULAR,
        chunk_size: int = 120000,
        token_counter: Callable[[str], int] | None = None,
        initial_script: Callable[[Page], Awaitable[Page]] | None = None,
        stealth: bool = True,
    ):
        """Initialize Parsera

        Args:
            model (BaseChatModel | None, optional): LangChain Chat Model. Defaults to None which invokes usage of
                GPT4oMiniModel.
            extractor (ExtractorType, optional): Extractor type from the ExtractorType enum. Defaults to ExtractorType.TABULAR.
            chunk_size (int, optional): Number of tokens per chunk, should be below context size of the model used. Defaults to 120000.
            token_counter (Callable[[str], int] | None, optional): Function used to estimate number of tokens in chunks.
                If None will use OpenAI tokenizer for gpt-4o model. Defaults to None.
        """
        if model is None:
            self.model = GPT4oMiniModel()
        else:
            self.model = model
        if token_counter is None:

            def count_tokens(text):
                # Initialize the tokenizer for GPT-4o-mini
                encoding = tiktoken.get_encoding("o200k_base")

                # Count tokens
                tokens = encoding.encode(text)
                return len(tokens)

            self._token_counter = count_tokens
        else:
            self._token_counter = token_counter
        self.extractor = extractor
        self.chunk_size = chunk_size

        self.loader = PageLoader()
        self.extractor_instance = None
        self.initial_script = initial_script
        self.stealth = stealth

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

        self.extractor_instance = self.extractor.value(
            elements=elements,
            model=self.model,
            content=content,
            chunk_size=self.chunk_size,
            token_counter=self._token_counter,
        )
        result = await self.extractor_instance.run()
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
