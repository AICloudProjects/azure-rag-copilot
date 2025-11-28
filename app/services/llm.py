#app/services/llm.py
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

# Managed Identity (no API key needed)
credential = DefaultAzureCredential()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    azure_ad_token_provider=credential.get_token
)


def generate_answer(context: str, question: str):
    """
    Generates a grounded answer using Azure OpenAI chat completion.
    Uses Managed Identity authentication (Week 4).
    """

    messages = [
        {"role": "system", 
         "content": "You are a helpful RAG assistant. Use ONLY the provided context. "
                    "If the answer isn't in the context, say you don't know."},
        
        {"role": "user", 
         "content": f"Context:\n{context}\n\nUser question: {question}"}
    ]

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2   # <-- Added for stable deterministic RAG answers
    )

    answer = resp.choices[0].message.content
    usage = resp.usage

    return answer, usage
