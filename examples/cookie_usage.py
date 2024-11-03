import asyncio
import json

from playwright.async_api import Page

from parsera import Parsera
from parsera.engine.model import GPT4oMiniModel

"""
Here's the example how you can provide custom cookie to Parsera!
Just add file with cookies (you really need to find your way how to find cookie) from you favourite website and that's it!
Note, that if website doesn't use cookies, this method won't work :(
"""


async def get_reddit_name():
    model = GPT4oMiniModel()

    file_with_cookeis = "cookies.json"
    with open(file_with_cookeis, "r") as file:
        cookies = json.load(file)

    parsera = Parsera(model=model, custom_cookies=cookies)
    return await parsera.arun(
        url="https://www.reddit.com/settings/",
        elements={
            "email address": "value",
        },
    )


if __name__ == "__main__":
    result = asyncio.run(get_reddit_name())
    print(result)
