# app/services/search.py

import os
import requests

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_INDEX_NAME = os.getenv("AZURE_INDEX_NAME", "documents-index")
SEARCH_API_VERSION = os.getenv("SEARCH_API_VERSION", "2024-05-01-preview")

#HEADERS = {
   # "Content-Type": "application/json",
   # "api-key": AZURE_SEARCH_KEY
#}

from azure.identity import DefaultAzureCredential
import os
import requests

credential = DefaultAzureCredential()

def get_search_headers():
    token = credential.get_token("https://search.azure.com/.default").token
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


def vector_search(embedding: list, k: int = 3):
    """Perform Azure Cognitive Search vector search"""

    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_INDEX_NAME}/docs/search?api-version={SEARCH_API_VERSION}"

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

   # resp = requests.post(url, headers=HEADERS, json=body)
     headers = get_search_headers()
     resp = requests.post(url, headers=headers, json=body)

    if resp.status_code not in (200, 201):
        raise Exception(f"Vector search error {resp.status_code}: {resp.text}")

    return resp.json()
