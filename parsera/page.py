import asyncio
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
    def __init__(self, browser: Browser | None = None):
        self.playwright: Playwright | None = None
        self.browser: Browser | None = browser
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    async def new_browser(self) -> None:
        if not self.playwright:
            self.playwright = await async_playwright().start()

        if self.browser:
            await self.browser.close()

        self.browser = await self.playwright.firefox.launch(headless=True)

    async def stealth(
        self,
        page: Page,
        proxy_settings: ProxySettings | None,
    ) -> Page:
        user_agent = await self.page.evaluate("navigator.userAgent")
        user_agent = user_agent.replace("HeadlessChrome/", "Chrome/")
        await self.context.close()

        self.context = await self.browser.new_context(
            user_agent=user_agent, proxy=proxy_settings
        )
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
            self.page = await self.stealth(
                page=self.page, proxy_settings=proxy_settings
            )

        if playwright_script:
            self.page = await playwright_script(self.page)

    async def fetch_page(
        self,
        url: str,
        scrolls_limit: int = 0,
        load_state: Literal[
            "domcontentloaded", "load", "networkidle"
        ] = "domcontentloaded",
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ) -> None:
        # Navigate to the URL
        await self.page.goto(url)
        await self.page.wait_for_load_state(load_state)

        if playwright_script:
            self.page = await playwright_script(self.page)

        # Start tracking removed content with MutationObserver
        await self.page.evaluate(
            """
            window.removedContent = [];
            const observer = new MutationObserver((mutations) => {
                mutations.forEach(mutation => {
                    if (mutation.removedNodes.length > 0) {
                        mutation.removedNodes.forEach(node => {
                            if (node.nodeType === 1) { // Only store element nodes
                                window.removedContent.push(node.outerHTML);
                            }
                        });
                    }
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });
        """
        )

        # Function to perform the scrolling
        scrolls = 0
        last_height = 0
        captured_content = []

        while scrolls < scrolls_limit:
            # Scroll down to the bottom of the page
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for page to load
            await asyncio.sleep(2)

            # Capture current visible content and append to the list
            current_content = await self.page.content()
            captured_content.append(current_content)

            # Check current scroll height
            new_height = await self.page.evaluate("document.body.scrollHeight")

            # Break if no new content is loaded (based on scroll height)
            if new_height == last_height:
                break

            last_height = new_height
            scrolls += 1

        # Fetch removed content if any
        removed_content = await self.page.evaluate("window.removedContent.join('')")

        # Combine all the captured content, including removed elements
        final_content = "".join(captured_content) + removed_content

        return final_content

    async def load_content(
        self,
        url: str,
        scrolls_limit: int = 0,
        proxy_settings: ProxySettings | None = None,
        load_state: Literal[
            "domcontentloaded", "load", "networkidle"
        ] = "domcontentloaded",
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ):
        await self.create_session(proxy_settings=proxy_settings)
        return await self.fetch_page(
            url=url,
            scrolls_limit=scrolls_limit,
            load_state=load_state,
            playwright_script=playwright_script,
        )

    async def close(self) -> None:
        if self.playwright:
            await self.browser.close()
            self.playwright.stop()
