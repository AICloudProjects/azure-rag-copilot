import os
import json
import requests
from openai import AzureOpenAI

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_INDEX_NAME = os.getenv("AZURE_INDEX_NAME", "documents-index")
SEARCH_API_VERSION = os.getenv("SEARCH_API_VERSION", "2024-05-01-preview")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-05-01-preview"
)

HEADERS = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_KEY
}

def get_embedding(text: str):
    text = text[:8000]
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return resp.data[0].embedding

def vector_search(query: str, k: int = 3):
    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_INDEX_NAME}/docs/search?api-version={SEARCH_API_VERSION}"

    emb = get_embedding(query)

    body = {
        "vectorQueries": [
            {
                "kind": "vector",
                "vector": emb,
                "fields": "embedding",
                "k": k
            }
        ],
        "select": "id, content, source"
    }

    print("Sending search request...")
    resp = requests.post(url, headers=HEADERS, json=body)

    print("Status:", resp.status_code)
    print("Response:", resp.text)

    if resp.status_code not in (200, 201):
        raise Exception(f"Search failed: {resp.text}")

    return resp.json()

if __name__ == "__main__":
    print("Testing vector search...")
    results = vector_search("What is Azure Cognitive Search?")

    print("\n==== RESULTS ====")
    for r in results.get("value", []):
        print(f"- {r['id']}: {r['content'][:120]}...")
