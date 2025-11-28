# app/services/embeddings.py

import os
from openai import AzureOpenAI

# Azure OpenAI client (embedding + chat)
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


def embed_text(text: str) -> list:
    """Return embedding vector from Azure OpenAI"""
    text = (text or "")[:8000]

    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return resp.data[0].embedding
