import os
import json
import glob
import requests
from openai import AzureOpenAI

# --------------------------
# Load ENV settings
# --------------------------
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")   
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_INDEX_NAME = os.getenv("AZURE_INDEX_NAME", "documents-index")
SEARCH_API_VERSION = os.getenv("SEARCH_API_VERSION", "2024-05-01-preview")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-05-01-preview"
)

HEADERS = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_KEY
}

# --------------------------
# Helper: Clean content
# --------------------------
def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")  # null chars if any
    return text.strip()


# --------------------------
# Helper: Generate embedding
# --------------------------
def get_embedding(text: str):
    text = text[:8000]  # safety cap
    resp = client.embeddings.create(
        model=embedding_model,
        input=text
    )
    emb = resp.data[0].embedding
    return emb


# --------------------------
# Upload documents to Azure Search
# --------------------------
def upload_documents():
    if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_KEY:
        raise Exception("Search endpoint or key missing")

    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_INDEX_NAME}/docs/index?api-version={SEARCH_API_VERSION}"

    batch = {"value": []}

    # Read all text files in data/
    for path in glob.glob("data/*.txt"):
        with open(path, "r", encoding="utf-8") as f:
            content = clean_text(f.read())

        # Generate embedding
        print(f"Generating embedding for {path}...")
        embedding = get_embedding(content)

        # Prepare document for index
        base = os.path.basename(path)
        doc_id = os.path.splitext(base)[0]
        doc_id = (
            doc_id.replace(".", "_")
                  .replace(" ", "_")
                  .replace("/", "_")
                  .replace("\\", "_")
        )

        batch["value"].append({
            "@search.action": "upload",
            "id": doc_id,
            "content": content,
            "source": path,
            "embedding": embedding
        })

    # Send upload request
    print(f"Uploading {len(batch['value'])} documents...")
    resp = requests.post(url, headers=HEADERS, json=batch)

    print("Status:", resp.status_code)
    print("Response:", resp.text)

    if resp.status_code not in (200, 201):
        raise Exception(f"Failed to upload documents: {resp.text}")

    print("Documents uploaded successfully!")


# --------------------------
# Main entry
# --------------------------
if __name__ == "__main__":
    print("Starting upload process...")
    upload_documents()
