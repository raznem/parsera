## Custom browser usage

You can setup playwright browser with custom parameters for development puposes and use it with Parsera!

```python
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, slow_mo=100)
        loader = PageLoader(browser=browser)
        await loader.create_session()
        content = await loader.fetch_page(url=url)
        return content
```

In this example you can try how to use browser with the custom options such as slow mode and window mode.

[Check out full example](https://github.com/raznem/parsera/tree/main/examples/infinite_page_scrolling.py)