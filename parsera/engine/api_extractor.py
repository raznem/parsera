import os
import warnings
from abc import ABC, abstractmethod

import requests

API_ENDPOINT = "https://api.parsera.org/v1/parse"


class Extractor(ABC):
    @abstractmethod
    async def run(
        self, content: str, attributes: dict[str, str] | None, prompt: str
    ) -> list[dict]:
        pass


class APIExtractor(Extractor):
    async def run(
        self,
        content: str,
        attributes: dict[str, str] | None = None,
        prompt: str = "",
        mode: str = "standard",
    ) -> list[dict]:
        if attributes is None and len(prompt) == 0:
            raise ValueError("At least prompt or attributes has to be provided")
        data = {
            "content": content,
            "prompt": prompt,
            "mode": mode,
        }

        if attributes:
            api_attributes = []
            for key, value in attributes.items():
                api_attributes.append({"name": key, "description": value})
            data["attributes"] = api_attributes

        parsera_api_key = os.getenv("PARSERA_API_KEY")
        headers = {"Content-Type": "application/json", "X-API-KEY": parsera_api_key}

        response = requests.post(API_ENDPOINT, headers=headers, json=data, timeout=180)
        response.raise_for_status()

        # Extract data from the response JSON
        response_json = response.json()
        if "detail" in response_json:  # API error reported in the response
            warnings.warn(response_json["detail"])

        return response_json.get("data", [])
