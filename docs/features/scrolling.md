## Page scrolling

[Parsera library](https://github.com/raznem/parsera) can scroll pages now!. To do this you simply should set parameter `scrolls_limit`.

This parameters is available for the `run` and `arun` methods in the `Parsera` class instance.

Check out the example below!:
```python
async def get_reddit_info():
    model = GPT4oMiniModel()

    parsera = Parsera(model=model)
    return await parsera.arun(
        url="https://www.reddit.com/",
        elements={
            "post name": "post description"
        },
        scrolls_limit = 10
    )
```