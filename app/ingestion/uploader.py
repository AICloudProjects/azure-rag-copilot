import os
import requests
from typing import List, Dict
from app.services.search import get_search_headers

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_INDEX_NAME = os.getenv("AZURE_INDEX_NAME", "documents-index")
SEARCH_API_VERSION = os.getenv("SEARCH_API_VERSION", "2024-05-01-preview")

def _chunk_batches(items: List[Dict], batch_size: int = 100):
    for i in range(0, len(items), batch_size):
        yield items[i:i+batch_size]

def upload_documents(docs: List[Dict]):
    if not docs:
        print("No documents to upload.")
        return

    url = (
        f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_INDEX_NAME}"
        f"/docs/index?api-version={SEARCH_API_VERSION}"
    )

    headers = get_search_headers()

    print(f"Uploading {len(docs)} documents to {AZURE_INDEX_NAME}...")

    for batch in _chunk_batches(docs, 100):
        actions = [
            {
                "@search.action": "upload",
                "id": d["id"],
                "content": d["content"],
                "source": d["source"],
                "embedding": d["embedding"],
            }
            for d in batch
        ]

        resp = requests.post(url, headers=headers, json={"value": actions})

        if resp.status_code not in (200, 201):
            raise Exception(
                f"Upload failed {resp.status_code}: {resp.text}"
            )

    print("Upload completed successfully.")
