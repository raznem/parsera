import asyncio

from playwright.async_api import Page

from parsera import ParseraScript
from parsera.engine.model import GPT4oMiniModel

EMAIL = "<YOUR-EMAIL>"
PASSWORD = "<YOUR-PASSWORD>"


async def get_parsera_credits():
    model = GPT4oMiniModel()

    # Define the script to execute during the session creation
    async def initial_script(page: Page) -> Page:
        await page.goto("https://parsera.org/auth/sign-in")
        await page.wait_for_load_state("networkidle")
        await page.get_by_label("Email").fill(EMAIL)
        await page.get_by_label("Password").fill(PASSWORD)
        await page.get_by_role("button", name="Sign In", exact=True).click()
        await page.wait_for_selector("text=Playground")
        return page

    # This script is executed after the url is opened
    async def repeating_script(page: Page) -> Page:
        await page.wait_for_timeout(1000)  # Wait one second for page to load
        return page

    parsera = ParseraScript(model=model, initial_script=initial_script)
    return await parsera.arun(
        url="https://parsera.org/app",
        elements={
            "credits": "number of credits",
        },
        playwright_script=repeating_script,
    )


if __name__ == "__main__":
    result = asyncio.run(get_parsera_credits())
    print(result)
