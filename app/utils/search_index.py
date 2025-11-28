import os
import requests
import json

# Load environment variables
AZURE_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")  
AZURE_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = os.getenv("AZURE_INDEX_NAME", "documents-index")
API_VERSION = os.getenv("SEARCH_API_VERSION", "2024-05-01-preview")

HEADERS = {
    "Content-Type": "application/json",
    "api-key": AZURE_KEY
}

# --------------------------------------------------------------------
# FINAL VALID INDEX SCHEMA FOR API VERSION 2024-05-01-PREVIEW
# --------------------------------------------------------------------
INDEX_SCHEMA = {
    "name": INDEX_NAME,
    "fields": [
        {
            "name": "id",
            "type": "Edm.String",
            "key": True,
            "filterable": True,
            "searchable": False
        },
        {
            "name": "content",
            "type": "Edm.String",
            "searchable": True
        },
        {
            "name": "source",
            "type": "Edm.String",
            "filterable": True,
            "searchable": False
        },
        {
            "name": "embedding",
            "type": "Collection(Edm.Single)",
            "searchable": True,
            "dimensions": 1536,
            "vectorSearchProfile": "vector-profile-1"
        }
    ],
    "vectorSearch": {
        "algorithms": [
            {
                "name": "hnsw-alg",
                "kind": "hnsw"
            }
        ],
        "profiles": [
            {
                "name": "vector-profile-1",
                "algorithm": "hnsw-alg"
            }
        ]
    }
}


# --------------------------------------------------------------------
# CREATE INDEX FUNCTION
# --------------------------------------------------------------------
def create_index():
    if not AZURE_ENDPOINT or not AZURE_KEY:
        raise ValueError("Missing AZURE_SEARCH_ENDPOINT or AZURE_SEARCH_KEY")

    url = f"{AZURE_ENDPOINT}/indexes/{INDEX_NAME}?api-version={API_VERSION}"

    print(f"PUT {url}")
    print("Sending schema:")
    print(json.dumps(INDEX_SCHEMA, indent=2))

    resp = requests.put(url, headers=HEADERS, json=INDEX_SCHEMA)

    print("Status:", resp.status_code)
    print("Response:", resp.text)

    if resp.status_code not in (200, 201):
        raise Exception(f"Failed to create index: {resp.text}")

    print("Index created successfully.")
    return resp.json()


# --------------------------------------------------------------------
# MAIN (run using: python3 -m app.utils.search_index)
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("Creating Azure Search index...")
    create_index()
