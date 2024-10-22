## Custom browser usage

You can setup playwright browser with custom parameters for development puposes and use it with Parsera!

```python
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, slow_mo=100)
        loader = PageLoader(browser=browser)
        content = await loader.load_content(url=url, scrolls_limit=10)
        return content
```

[Check out full example](https://github.com/raznem/parsera/tree/main/examples/infinite_page_scrolling.py)