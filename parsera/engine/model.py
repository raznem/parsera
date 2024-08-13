import os

from langchain_openai import AzureChatOpenAI, ChatOpenAI

from parsera.utils import singleton


@singleton
class AzureModel(AzureChatOpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(
            azure_endpoint=os.getenv("AZURE_GPT_BASE_URL"),
            openai_api_version="2023-05-15",
            deployment_name=os.getenv("AZURE_GPT_DEPLOYMENT_NAME"),
            openai_api_key=os.getenv("AZURE_GPT_API_KEY"),
            openai_api_type="azure",
            temperature=0.0,
            timeout=120,
            *args,
            **kwargs,
        )


@singleton
class GPT4oMiniModel(ChatOpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(
            model="gpt-4o-mini",
            temperature=0.0,
            timeout=120,
            *args,
            **kwargs,
        )
