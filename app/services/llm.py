# app/services/llm.py

import os
from openai import AzureOpenAI

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    azure_ad_token_provider=credential.get_token
)

#client = AzureOpenAI(
   # api_key=os.getenv("OPENAI_API_KEY"),
   # azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
   # api_version="2024-05-01-preview"
#)


def generate_answer(context: str, question: str):
    """
    Generates a grounded answer using Azure OpenAI chat completion.
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use ONLY the provided context."},
        {"role": "user", "content": f"Context:\n{context}\n\nUser question: {question}"}
    ]

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages
    )

    answer = resp.choices[0].message.content
    usage = resp.usage

    return answer, usage

