import warnings
from typing import Awaitable, Callable, Literal, TypedDict

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import StealthConfig, stealth_async


class ProxySettings(TypedDict, total=False):
    server: str
    bypass: str | None = None
    username: str | None = None
    password: str | None = None


class PageLoader:
    def __init__(
        self,
        browser: Literal["firefox", "chromium"] = "firefox",
    ):
        self._browser_id = browser
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    async def new_browser(self) -> None:
        if not self.playwright:
            self.playwright = await async_playwright().start()

        if self.browser:
            await self.browser.close()

        if self._browser_id == "firefox":
            self.browser = await self.playwright.firefox.launch(headless=True)
        else:
            self.browser = await self.playwright.chromium.launch(headless=True)

    async def stealth(self, page: Page) -> Page:
        user_agent = await self.page.evaluate("navigator.userAgent")
        user_agent = user_agent.replace("HeadlessChrome/", "Chrome/")
        await self.context.close()

        self.context = await self.browser.new_context(user_agent=user_agent)
        page = await self.context.new_page()
        await stealth_async(page, config=StealthConfig(navigator_user_agent=False))
        return page

    async def create_session(
        self,
        proxy_settings: ProxySettings | None = None,
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
        stealth: bool = True,
    ) -> None:
        if not self.browser:
            await self.new_browser()
        self.context = await self.browser.new_context(proxy=proxy_settings)
        self.page = await self.context.new_page()
        if stealth:
            self.page = await self.stealth(page=self.page)

        if playwright_script:
            self.page = await playwright_script(self.page)

    async def fetch_page(
        self,
        url: str,
        load_state: Literal[
            "domcontentloaded", "load", "networkidle"
        ] = "domcontentloaded",
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ) -> None:
        # Navigate to the URL
        # await page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort()) # Can speed up requests
        await self.page.goto(url)
        await self.page.wait_for_load_state(load_state)
        if playwright_script:
            self.page = await playwright_script(self.page)

        return await self.page.content()

    async def load_content(
        self,
        url: str,
        proxy_settings: ProxySettings | None = None,
        load_state: Literal[
            "domcontentloaded", "load", "networkidle"
        ] = "domcontentloaded",
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ):
        await self.create_session(proxy_settings=proxy_settings)
        return await self.fetch_page(
            url=url, load_state=load_state, playwright_script=playwright_script
        )

    async def close(self) -> None:
        if self.playwright:
            await self.browser.close()
            self.playwright.stop()


async def fetch_page_content(
    url: str,
    proxy_settings: ProxySettings | None = None,
    browser: str = "firefox",
) -> str:
    warnings.warn(
        "fetch_page_content is deprecated and will be removed",
        DeprecationWarning,
    )
    async with async_playwright() as p:
        # Launch the browser
        if browser == "firefox":
            browser = await p.firefox.launch(headless=True)
        else:
            browser = await p.chromium.launch(headless=True)
        # Open a new browser context
        context = await browser.new_context(proxy=proxy_settings)
        # Open a new page
        page = await context.new_page()
        await stealth_async(page)

        # Navigate to the URL
        # await page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort()) # Can speed up requests
        await page.goto(url)

        # Wait for the content to be dynamically loaded
        await page.wait_for_load_state("domcontentloaded")
        # Get the page content
        content = await page.content()

        # Close the browser
        await browser.close()

        return content
