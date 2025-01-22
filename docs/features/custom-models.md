Note that small local models tend to trim long outputs and could require more careful tuning of data description. 

## Run custom langchain OpenAI model

You can instantiate `Parsera` with any chat model supported by LangChain, for example, to run the model from Azure:  
```python
import os
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_GPT_BASE_URL"),
    openai_api_version="2023-05-15",
    deployment_name=os.getenv("AZURE_GPT_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("AZURE_GPT_API_KEY"),
    openai_api_type="azure",
    temperature=0.0,
)

url = "https://github.com/raznem/parsera"
elements = {
    "Stars": "Number of stars",
    "Fork": "Number of forks",
}
scrapper = Parsera(model=llm)
result = scrapper.run(url=url, elements=elements)
```

## Run local model with `Ollama`
First, you should install and run `ollama` in your local environment: [official installation guide](https://github.com/ollama/ollama?tab=readme-ov-file#ollama).
Additionally, you need to install `langchain_ollama` with:
```shell
pip install langchain-ollama
```

The next step is pulling the [model](https://ollama.com/search). For example, to pull Qwen2.5 14B run:
```shell
ollama pull qwen2.5:14b
```

After all the setup simply run:
```python
from parsera import Parsera
from langchain_ollama import ChatOllama

url = "https://github.com/raznem/parsera"
elements = {
    "Stars": "Number of stars",
    "Fork": "Number of forks",
}

llm = ChatOllama(
    model="qwen2.5:14b",
    temperature=0,
)

scrapper = Parsera(model=llm)
result = await scrapper.arun(url=url, elements=elements)
```


## Run local model with `Trasformers`
Currently, we only support models that include a `system` token

> You should install `Transformers` with either `pytorch` (recommended) or `TensorFlow 2.0`

[Transformers Installation Guide](https://huggingface.co/docs/transformers/en/installation)

Example:
```python
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from parsera.engine.model import HuggingFaceModel
from parsera import Parsera

# Define the URL and elements to scrape
url = "https://github.com/raznem/parsera"
elements = {
    "Stars": "Number of stars",
    "Fork": "Number of forks",
}

# Initialize model with transformers pipeline
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-128k-instruct", trust_remote_code=True)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=5000)

# Initialize HuggingFaceModel
llm = HuggingFaceModel(pipeline=pipe)

# Scrapper with HuggingFace model
scrapper = Parsera(model=llm)
result = scrapper.run(url=url, elements=elements)
```