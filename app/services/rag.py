# app/services/rag.py

from app.services.embeddings import embed_text
from app.services.search import vector_search
from app.services.llm import generate_answer

SYSTEM_PROMPT = (
    "You are a helpful RAG assistant. "
    "Use ONLY the provided context. "
    "If the answer is not in the context, say you don't know. "
)

def answer_question(query: str):
    """Full RAG pipeline: embed → search → context → LLM"""

    # 1. Embed the query
    embedding = embed_text(query)

    # 2. Retrieve top documents
    results = vector_search(embedding, k=3)   # <-- results is a LIST now

    # 3. Build context from retrieved docs
    context = "\n\n---\n\n".join(
        doc.get("content", "") for doc in results
    )

    # 4. Call Azure OpenAI (Managed Identity)
    answer, usage = generate_answer(context, query)

    # 5. Track which sources were used
    sources = [doc.get("source") for doc in results]

    return {
        "answer": answer,
        "usage": usage,
        "sources": sources
    }
