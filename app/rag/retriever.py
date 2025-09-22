# app/rag/retriever.py
from typing import List
from app.rag.vectorstore import get_vectorstore

def retrieve(query: str, k: int = 4) -> List[str]:
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=k)
    return [d.page_content for d in docs]

def stuff_context(question: str) -> str:
    chunks = retrieve(question, k=4)
    if not chunks:
        return ""
    header = "\n\n[Contexto de guías/recursos internos]\n"
    return header + "\n\n".join(f"• {c}" for c in chunks)
