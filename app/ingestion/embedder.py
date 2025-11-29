import hashlib
from typing import Dict, List
from app.services.embeddings import embed_text

def file_fingerprint(content: str) -> str:
    h = hashlib.sha256()
    h.update((content or "").encode("utf-8"))
    return h.hexdigest()[:16]

def build_index_documents(doc: Dict, chunks: List[Dict]) -> List[Dict]:
    source_path = doc["path"]
    content = doc["content"]
    fingerprint = file_fingerprint(content)

    index_docs = []

    for c in chunks:
        chunk_id = c["chunk_id"]
        text = c["text"]

        embedding = embed_text(text)

        index_docs.append({
            "id": f"{fingerprint}-{chunk_id:04d}",
            "content": text,
            "source": source_path,
            "embedding": embedding
        })

    return index_docs
