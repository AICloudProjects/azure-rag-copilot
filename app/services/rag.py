# app/services/rag.py
from app.services.embeddings import embed_text
from app.services.search import vector_search
from app.services.llm import generate_answer

def answer_question(query: str):

    # 1. embed
    embedding = embed_text(query)

    # 2. search
    results = vector_search(embedding, k=3)

    # 3. build context
    context = "\n".join(
        f"- {doc['content']}" for doc in results.get("value", [])
    )

    # 4. call LLM
    answer, usage = generate_answer(context, query)

    return answer, usage
