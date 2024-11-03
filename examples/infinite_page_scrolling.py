import asyncio

from playwright.async_api import async_playwright

from parsera.page import PageLoader

"""
Here's the example how you can load webpage of any length even with the custom browser parameters!
"""


async def main(url):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, slow_mo=100)
        loader = PageLoader(browser=browser)
        await loader.create_session()
        content = await loader.fetch_page(url=url, scrolls_limit=10)
        return content


if __name__ == "__main__":
    URL = "https://www.reddit.com/"
    result = asyncio.run(main(URL))
    print(result)
