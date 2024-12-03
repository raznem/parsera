import asyncio
from typing import Awaitable, Callable, Literal, TypedDict

from playwright.async_api import Browser, BrowserContext, Page, Playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright
from playwright_stealth import StealthConfig, stealth_async


class PageGotoError(Exception):
    pass


class CookiesValidationException(Exception):
    pass


class ProxySettings(TypedDict, total=False):
    server: str
    bypass: str | None = None
    username: str | None = None
    password: str | None = None


class PageLoader:
    def __init__(
        self, browser: Browser | None = None, custom_cookies: list[dict] | None = None
    ):
        self.playwright: Playwright | None = None
        self.browser: Browser | None = browser
        self.custom_cookies: list[dict] | None = custom_cookies
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    async def new_browser(self) -> None:
        if not self.playwright:
            self.playwright = await async_playwright().start()

        if self.browser:
            await self.browser.close()

        # slow_mo mode is just only to deal with js rendering
        self.browser = await self.playwright.firefox.launch(headless=True)

    async def stealth(
        self,
        page: Page,
        proxy_settings: ProxySettings | None,
    ) -> Page:
        user_agent = await page.evaluate("navigator.userAgent")
        user_agent = user_agent.replace("HeadlessChrome/", "Chrome/")
        await self.context.close()

        self.context = await self.browser.new_context(
            user_agent=user_agent, proxy=proxy_settings
        )
        if self.custom_cookies is not None:
            try:
                await self.context.add_cookies(self.custom_cookies)
            except Exception as exc:
                raise CookiesValidationException(str(exc)) from exc
        page = await self.context.new_page()
        await stealth_async(
            page,
            config=StealthConfig(
                navigator_user_agent=False,
                navigator_plugins=False,
                navigator_vendor=False,
            ),
        )

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

        if self.custom_cookies is not None:
            try:
                await self.context.add_cookies(self.custom_cookies)
            except Exception as exc:
                raise CookiesValidationException(str(exc)) from exc
        self.page = await self.context.new_page()
        if stealth:
            self.page = await self.stealth(
                page=self.page, proxy_settings=proxy_settings
            )

        if playwright_script:
            self.page = await playwright_script(self.page)

    async def scroll_page(self, scrolls_limit: int = 0):
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

    async def get_iframe_html(self, frame):
        try:
            if frame.is_detached():  # Skip detached frames
                return None
            return await frame.evaluate("document.documentElement.outerHTML")
        except Exception as e:
            print(f"Could not access iframe: {e}")
            return None

    async def get_full_html(self):
        # Get main document HTML
        main_html = await self.page.evaluate("document.documentElement.outerHTML")

        # Fetch all iframe HTMLs in parallel
        iframe_html_tasks = [self.get_iframe_html(frame) for frame in self.page.frames[1:]]
        iframes_html = await asyncio.gather(*iframe_html_tasks)

        # Filter out None values (failed iframe retrievals)
        iframes_html = [html for html in iframes_html if html is not None]

        # Combine main HTML and iframe HTML into one variable
        combined_html = f"<!-- Main Page HTML -->\n{main_html}\n"
        for idx, iframe_html in enumerate(iframes_html):
            combined_html += f"\n<!-- Iframe {idx + 1} HTML -->\n{iframe_html}\n"

        return combined_html

    async def fetch_page(
        self,
        url: str,
        scrolls_limit: int = 0,
        load_state: Literal["domcontentloaded", "load", "networkidle"] = "networkidle",
        playwright_script: Callable[[Page], Awaitable[Page]] | None = None,
    ) -> None:
        # Navigate to the URL
        try:
            await self.page.goto(url)
        except Exception as exc:
            raise PageGotoError(str(exc)) from exc
        try:
            await self.page.wait_for_load_state(load_state)
        except PlaywrightTimeoutError:
            pass

        if playwright_script:
            self.page = await playwright_script(self.page)

        # peform scrolling
        if scrolls_limit > 0:
            result = await self.scroll_page(scrolls_limit)
        else:
            result = await self.get_full_html()

        return result

    async def close(self) -> None:
        if self.playwright:
            await self.context.close()
            await self.browser.close()
            await self.playwright.stop()
