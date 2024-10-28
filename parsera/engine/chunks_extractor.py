import json
import math
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from markdownify import markdownify

from parsera.engine.simple_extractor import Extractor

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

If value for the field is not found use `null` in the json:
```json
[
    {"name": "name1", "price": "100"},
    {"name": "name2", "price": null},
    {"name": "name3", "price": "300"},
]
```

If no data is found return empty json:
```json
[]
```

"""


SYSTEM_MERGE_PROMPT_TEMPLATE = """
Your goal is to merge data extracted from different parts of the page into one json.
Keep the original structure, but make sure to correctly merge data to not have duplicates, prefer rows with more data.

In case of conflicting values, take the data that is further from the boarder between the files.
## Example: merging conflicting values
```
[
    {"name": "zero element", "price": "123"},
    {"name": "first element", "price": "100"},
    {"name": "second element", "price": "200"},
    {"name": "third element", "price": "999"},
]
```

and 

```
[
    {"name": "second element", "price": "123"},
    {"name": "third element", "price": "400"},
]
```

In the case above the "second element"'s price should be taken from the first json, cause it's further from the boarder
between the files, while "third element"'s price should be taken from the second json. The final output should be:

Merged json:
```
[
    {"name": "zero element", "price": "123"},
    {"name": "first element", "price": "100"},
    {"name": "second element", "price": "200"},
    {"name": "third element", "price": "400"},
]
```

## Example: merging missing values
```
[
    {"name": "zero element", "price": "123"},
    {"name": "first element", "price": "100"},
    {"name": "second element", "price": "200"},
    {"name": "third", "price": null},
]
```

and 

```
[
    {"name": "second element", "price": "123"},
    {"name": "third element", "price": "400"},
    {"name": "fourth element", "price": "350"},
]
```

In this case the "third element" should be taken from the second json, because it contains missing value for the "price"
and fixed truncated name "third". The final output should be:

Merged json:
```
[
    {"name": "zero element", "price": "123"},
    {"name": "first element", "price": "100"},
    {"name": "second element", "price": "200"},
    {"name": "third element", "price": "400"},
    {"name": "fourth element", "price": "350"},
]
```

"""

EXTRACTOR_MERGE_PROMPT_TEMPLATE = """
Elements requested by user:
```
{elements}
```

All jsons from different parts of the page:
{jsons_list}

Merged json:
"""

APPEND_TABULAR_EXTRACTOR_SYSTEM_PROMPT = """
Your goal is to continue the sequence extracted from the previous chunk of the page by adding elements from the new page
chunk. Note, that chunks are overlapping, so the data extracted from the previous chunk can appear in the content again,
in this case always try to find values for the rows based on the content of the truncated page chunk provided by user. 
Output json should contain all records you observe on the page.

## Example: continue truncated json
Fill missing values, fix truncated values and continue this sequence:
```json
[
    {"name": "zero product", "price": "25"},
    {"name": "first product", "price": "100"},
    {"name": "second", "price": null},
]
```

Return the following elements from the truncated page chunk:
```
{
    "name": "name of the listing",
    "price": "price of the listing"
}
```

Make sure to fill mussing and truncated values in the previous sequence, while using `null` in the records where data
was not found. Like in example below, where price for the "fourth product" was not found.
Output json with fixed previous sequence and new rows:
```json
[
    {"name": "zero product", "price": "25"},
    {"name": "first product", "price": "100"},
    {"name": "second product", "price": "100"},
    {"name": "third product", "price": "150"},
    {"name": "fourth product", "price": null},
]
```

## Example: user asks for single field

User requesting the following elements from the truncated page chunk:
```
{
    "link": "link to the listing",
}
```
Make sure to return json with only this field
Output json with fixed previous sequence and new rows:
```json
[
    {"link": "https://example.com/link1"},
    {"link": "https://example.com/link2"},
    {"link": "https://example.com/link3"},
]
```

## Note

If no data is found return empty json:
```json
[]
```

"""

APPEND_EXTRACTOR_PROMPT_TEMPLATE = """
Fill missing values, fix truncated values and continue this sequence:
```
{previous_data}
```

The current truncated page chunk:
---
{markdown}
---

You are looking for the following elements from the truncated page chunk:
```
{elements}
```

Output json with fixed previous sequence and new rows:
"""


class ChunksTabularExtractor(Extractor):
    system_prompt = TABULAR_EXTRACTOR_SYSTEM_PROMPT
    system_merge_prompt = SYSTEM_MERGE_PROMPT_TEMPLATE
    prompt_merge_template = EXTRACTOR_MERGE_PROMPT_TEMPLATE
    append_system_prompt = APPEND_TABULAR_EXTRACTOR_SYSTEM_PROMPT
    append_prompt_template = APPEND_EXTRACTOR_PROMPT_TEMPLATE
    overlap_factor = 3

    def __init__(
        self,
        elements: dict,
        model: BaseChatModel,
        content: str,
        chunk_size: int,
        token_counter: Callable[[str], int],
    ):
        self.elements = elements
        self.model = model
        self.content = content
        # self.token_counter = token_counter
        self.chunk_size = chunk_size
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_size // self.overlap_factor,
            length_function=token_counter,
        )
        self.chunks_data = None

    async def extract(
        self, markdown: str, previous_data: list[dict] | None = None
    ) -> list[dict]:
        elements = json.dumps(self.elements)
        if not previous_data:
            human_msg = self.prompt_template.format(
                markdown=markdown, elements=elements
            )
        else:
            cutoff = math.ceil(len(previous_data) / self.overlap_factor)
            previous_tail = json.dumps(previous_data[cutoff:])
            human_msg = self.append_prompt_template.format(
                markdown=markdown, elements=elements, previous_data=previous_tail
            )
        messages = [
            SystemMessage(self.system_prompt),
            HumanMessage(human_msg),
        ]
        output = await self.model.ainvoke(messages)
        parser = JsonOutputParser()
        output_dict = parser.parse(output.content)
        return output_dict

    async def merge_all_data(self, all_data):
        elements = json.dumps(self.elements)
        json_list = ""
        for data in all_data:
            json_list += "``` \n" + json.dumps(data) + "\n ```\n"

        human_msg = self.prompt_merge_template.format(
            elements=elements, jsons_list=json_list
        )
        messages = [
            SystemMessage(self.system_merge_prompt),
            HumanMessage(human_msg),
        ]
        output = await self.model.ainvoke(messages)
        parser = JsonOutputParser()
        output_dict = parser.parse(output.content)
        return output_dict

    async def run(
        self,
    ) -> dict:
        if self.system_prompt is None:
            raise ValueError("system_prompt is not defined for this extractor")
        if self.prompt_template is None:
            raise ValueError("prompt_template is not defined for this extractor")

        markdown = markdownify(self.content)
        # chunks = chunk(
        #     text=markdown,
        #     chunk_size=self.chunk_size,
        #     token_counter=self.token_counter,
        #     memoize=False,
        # )
        chunks = self.text_splitter.create_documents([markdown])
        if len(chunks) > 1:
            self.chunks_data = []
            chunk_data = None
            for i, element in enumerate(chunks):
                chunk_data = await self.extract(
                    markdown=element, previous_data=chunk_data
                )
                self.chunks_data.append(chunk_data)

            output_dict = await self.merge_all_data(self.chunks_data)
        else:
            output_dict = await self.extract(markdown=chunks[0])

        return output_dict
