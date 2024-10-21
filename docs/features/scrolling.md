## Page scrolling

[Parsera library](https://github.com/raznem/parsera) can scroll pages now!. To do this you simply should set parameter `scrolls_limit`.

This parameters is available for the `run` and `arun` for `Parsera` and `ParseraScript` classes.

Check out the example below!:
```python
async def get_reddit_info():
    model = GPT4oMiniModel()

    # This script is executed after the url is opened
    async def pw_script(page: Page) -> Page:
        await page.wait_for_timeout(1000)  # Wait one second for page to load
        return page

    parsera = ParseraScript(model=model)
    return await parsera.arun(
        url="https://www.reddit.com/",
        elements={
            "post name": "post description"
        },
        playwright_script=pw_script,
        scrolls_limit = 10
    )
```