from typing import List, Dict
import tiktoken

def get_encoder():
    return tiktoken.get_encoding("cl100k_base")

def chunk_text(text: str, max_tokens: int = 500, overlap: int = 50) -> List[Dict]:
    enc = get_encoder()
    tokens = enc.encode(text or "")

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(tokens):
        end = start + max_tokens
        token_slice = tokens[start:end]
        chunk_text = enc.decode(token_slice)

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text
        })
        chunk_id += 1

        start = end - overlap
        if start < 0:
            start = 0

    return chunks
