# app/services/embeddings.py

import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential

# Managed Identity credential
credential = DefaultAzureCredential()

# Azure OpenAI client (keyless via Managed Identity)
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    azure_ad_token_provider=credential.get_token
)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


def embed_text(text: str) -> list:
    """
    Generate embeddings from Azure OpenAI using Managed Identity.
    Truncates text to 8000 chars for safety.
    """
    text = (text or "")[:8000]

    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return resp.data[0].embedding
