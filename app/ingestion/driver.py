import os

from app.ingestion.loader import iter_documents
from app.ingestion.chunker import chunk_text
from app.ingestion.embedder import build_index_documents
from app.ingestion.uploader import upload_documents

DATA_DIR = os.getenv("DATA_DIR", "data")

def run_batch_ingestion():
    print(f"Starting batch ingestion from data dir: {DATA_DIR}")

    all_chunks = []
    count = 0

    for doc in iter_documents(DATA_DIR):
        count += 1
        print(f"Processing: {doc['path']}")

        chunks = chunk_text(doc["content"])
        indexed = build_index_documents(doc, chunks)
        all_chunks.extend(indexed)

    print(f"Total PDFs: {count}")
    print(f"Total chunks: {len(all_chunks)}")

    upload_documents(all_chunks)

if __name__ == "__main__":
    run_batch_ingestion()
