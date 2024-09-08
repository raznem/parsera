## ParseraScript
With `ParseraScript` class you can execute custom playwright scripts during scraping. There are 2 types of code you can
run:

- `initial_script` which is executed during the first run of `ParseraScript`, useful when you need to log in to access the data.
- `playwright_script` which runs during every `run` call, which allows to do custom actions before data is extracted, useful when data is hidden behind some button.

## Example: log in and load data
You can log in to [parsera.org](https://parsera.org) and get credits amount with the following code:
```python
from playwright.async_api import Page
from parsera import ParseraScript

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
result = await parsera.arun(
    url="https://parsera.org/app",
    elements={
        "credits": "number of credits",
    },
    playwright_script=repeating_script,
)
```

## Access Playwright instance
The page is fetched via the `ParseraScript.loader`, which contains the playwright instance.
```python
from parsera import ParseraScript

parsera = ParseraScript(model=model)

## You can manually initialize playwright session and modify it:
await parsera.new_session()
await parsera.loader.load_content(url=url)

## After page is loaded you can access playwright elements, like Page:
parsera.loader.page.getByRole('button').click()

## Next you cun run extraction process
result = await parsera.arun(
    url=extraction_url,
    elements=elements_dict,
)
```
