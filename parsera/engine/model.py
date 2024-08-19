import os

from langchain_openai import AzureChatOpenAI, ChatOpenAI

from parsera.utils import singleton

from langchain.chat_models.base import BaseChatModel
from typing import List, Optional, Any
from langchain_core.outputs.chat_generation import ChatGeneration
from langchain_core.callbacks.manager import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain_core.outputs.chat_result import ChatResult
from langchain.chat_models.base import BaseMessage
from langchain_core.messages.ai import AIMessage
from functools import partial
import asyncio

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

@singleton
class HuggingFaceModel(BaseChatModel):
    """
    Model for using HuggingFace pipeline.

    Imports embeded in the class to avoid all users 
    from having to install necessary dependencies 
    for this model.
    """
    from transformers import pipeline
    from transformers import Pipeline

    pipeline: Pipeline

    def _generate(
    self,
    messages: List[BaseMessage],
    stop: Optional[List[str]] = None,
    run_manager: Optional[CallbackManagerForLLMRun] = None,
    **kwargs: Any,
    ) -> ChatResult:
        # Implement the logic for generating the response using the HuggingFace model
        output_str = self._call(messages, stop=stop, run_manager=run_manager, **kwargs)
        message = AIMessage(content=output_str)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])
    
    def _call(
    self,
    messages: List[BaseMessage],
    stop: Optional[List[str]] = None,
    run_manager: Optional[CallbackManagerForLLMRun] = None,
    **kwargs: Any,
    ) -> str:
        pipe = self.pipeline
        prompt = " ".join([message.content for message in messages])
        # Define the messages
        messages = [
            {"role": "user", "content": prompt}
        ]
        response = pipe(messages)
        generated_text = response[0]['generated_text'][-1]['content']
        return generated_text
    
    async def _agenerate(
    self,
    messages: List[BaseMessage],
    stop: Optional[List[str]] = None,
    run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
    **kwargs: Any,
    ) -> ChatResult:
        func = partial(
            self._generate, messages, stop=stop, run_manager=run_manager, **kwargs
        )
        return await asyncio.get_event_loop().run_in_executor(None, func)
    
    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model."""
        return "custom"
