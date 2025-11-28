# app/services/rag.py

import os
from openai import AzureOpenAI

from app.services.embeddings import embed_text
from app.services.search import vector_search


CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

# Azure OpenAI chat client
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)


def answer_question(query: str):
    """Full RAG pipeline: embed → search → build context → chat completion"""

    # 1. Embed user query
    embedding = embed_text(query)

    # 2. Vector search
    results = vector_search(embedding, k=3)

    # 3. Build context string
    context_chunks = [
        f"- {doc['content']}" for doc in results.get("value", [])
    ]
    context = "\n".join(context_chunks)

    # 4. Generate answer using Azure OpenAI
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use ONLY the context."},
        {"role": "user", "content": f"Context:\n{context}\n\nUser question: {query}"}
    ]

    chat_resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages
    )

    answer = chat_resp.choices[0].message.content

    usage = chat_resp.usage

    return answer, usage
