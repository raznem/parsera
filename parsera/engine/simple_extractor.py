import json

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from markdownify import markdownify

SIMPLE_EXTRACTOR_SYSTEM_PROMPT = """
Your goal is to find the elements from the webpage content and return them in json format.
For example if user asks:
Return the following elements from the page content:
```
{
    "name": "name of the listing",
    "price": "price of the listing"
}
```
Make sure to return json with the list of corresponding values.
Output json:
```json
{
    "names": ["name1", "name2", "name3"],
    "price": ["100", "150", "300"],
}
```
"""

SIMPLE_EXTRACTOR_PROMPT_TEMPLATE = """
Having following page content:
```
{markdown}
```

Return the following elements from the page content:
```
{elements}
```

Output json:
"""


class JsonExtractor:
    system_prompt = SIMPLE_EXTRACTOR_SYSTEM_PROMPT
    prompt_template = SIMPLE_EXTRACTOR_PROMPT_TEMPLATE

    def __init__(self, elements: dict, model: BaseChatModel, content: str):
        self.elements = elements
        self.model = model
        self.content = content

    async def run(self) -> dict:
        markdown = markdownify(self.content)

        elements = json.dumps(self.elements)
        human_msg = self.prompt_template.format(markdown=markdown, elements=elements)
        messages = [
            SystemMessage(self.system_prompt),
            HumanMessage(human_msg),
        ]
        output = await self.model.ainvoke(messages)
        parser = JsonOutputParser()
        output_dict = parser.parse(output.content)
        return output_dict


TABULAR_EXTRACTOR_SYSTEM_PROMPT = """
Your goal is to find the elements from the webpage content and return them in json format.
For example if user asks:
Return the following elements from the page content:
```
{
    "name": "name of the listing",
    "price": "price of the listing"
}
```
Make sure to return json with the list of corresponding values.
Output json:
```json
[
    {"name": "name1", "price": "100"},
    {"name": "name2", "price": "150"},
    {"name": "name3", "price": "300"},
]
```

If users asks for a single field:
Return the following elements from the page content:
```
{
    "link": "link to the listing",
}
```
Make sure to return json with only this field
Output json:
```json
[
    {"link": "https://example.com/link1"},
    {"link": "https://example.com/link2"},
    {"link": "https://example.com/link3"},
]
```

"""


class TabularExtractor(JsonExtractor):
    system_prompt = TABULAR_EXTRACTOR_SYSTEM_PROMPT
