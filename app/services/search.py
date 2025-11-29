# app/services/search.py

import os
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

def get_search_headers():
    token = credential.get_token("https://search.azure.com/.default")
    return {
        "Content-Type": "application/json",
        "api-key": None,
        "Authorization": f"Bearer {token.token}"
    }

def vector_search(embedding: list, k: int = 3):
    """
    Perform Azure Cognitive Search vector search using Managed Identity.
    """
    url = (
        f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_INDEX_NAME}"
        f"/docs/search?api-version={SEARCH_API_VERSION}"
    )

    body = {
        "vectorQueries": [
            {
                "kind": "vector",
                "vector": embedding,
                "fields": "embedding",
                "k": k
            }
        ],
        "select": "id, content, source"
    }

    headers = get_search_headers()
    resp = requests.post(url, headers=headers, json=body)

    if resp.status_code not in (200, 201):
        raise Exception(f"Vector search error {resp.status_code}: {resp.text}")

    # Return only the document array
    return resp.json().get("value", [])
