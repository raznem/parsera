import json
import math
from typing import Any, Callable, List, Literal, Optional, Type

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from markdownify import MarkdownConverter
from pydantic import BaseModel, Field, create_model

from parsera.engine.chunks_extractor import ChunksTabularExtractor
from parsera.utils import has_any_non_none_values


class AttributeData(BaseModel):
    description: str = ""
    type: Literal["string", "integer", "number", "bool", "list", "object", "any"] = (
        "any"
    )


type_mapping: dict[str, Type[Any]] = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
    "any": Any,
}


class StructuredExtractor(ChunksTabularExtractor):
    def __init__(
        self,
        model: BaseChatModel,
        chunk_size: int = 100000,
        token_counter: Callable[[str], int] | None = None,
        converter: MarkdownConverter | None = None,
    ):
        super().__init__(
            model=model,
            chunk_size=chunk_size,
            token_counter=token_counter,
            converter=converter,
        )
        self.structured_model: BaseChatModel | None = None

    async def extract(
        self,
        markdown: str,
        attributes: dict[str, str],
        previous_data: list[dict] | None = None,
    ) -> list[dict]:
        elements = json.dumps(attributes)
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
        structured_output = await self.structured_model.ainvoke(messages)
        output_dict = structured_output.model_dump(mode="json")
        if has_any_non_none_values(output_dict["data"]):
            return output_dict["data"]
        else:
            return []

    async def merge_all_data(
        self, all_data: list[list[dict]], attributes: dict[str, str]
    ) -> dict:
        elements = json.dumps(attributes)
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
        structured_output = await self.structured_model.ainvoke(messages)
        output_dict = structured_output.model_dump(mode="json")
        return output_dict["data"]

    def create_schema(self, attributes: dict[str, dict[str, Any]]) -> Type[BaseModel]:
        pydantic_fields: dict[str, Any] = {}
        for field_name, field_info in attributes.items():
            field_type = type_mapping.get(field_info["type"])
            if field_type is None:
                field_type = Any

            field_type = Optional[field_type]
            field_args = {"description": field_info["description"], "default": None}

            pydantic_fields[field_name] = (field_type, Field(**field_args))

        RecordModel = create_model(
            "AttributesFormatter",
            __base__=BaseModel,
            **pydantic_fields,
        )

        class ListSchemaModel(BaseModel):
            data: List[RecordModel] = Field(default_factory=list)

        return ListSchemaModel

    async def run(
        self,
        content: str,
        attributes: dict[str, dict[str, Any]],
    ) -> dict:
        for value in attributes.values():
            AttributeData.model_validate(value)
        OutputSchema = self.create_schema(attributes)
        self.structured_model = self.model.with_structured_output(schema=OutputSchema)
        output = await super().run(content=content, attributes=attributes)
        return output
