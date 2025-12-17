# import nest_asyncio

# nest_asyncio.apply()
import os

from parsera import Parsera

os.environ["PARSERA_API_KEY"] = "2a0f66562472d7b7b8155b08af1688d4"

url = "https://news.ycombinator.com/"
elements = {
    "Title": "News title",
    "Points": "Number of points",
    "Comments": "Number of comments",
}

print(os.getenv("PARSERA_API_KEY"))
scraper = Parsera()
result = scraper.run(url=url, elements=elements)
print(result)
