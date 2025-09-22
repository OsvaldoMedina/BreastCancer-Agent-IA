# app/rag/vectorstore.py
from langchain_community.vectorstores import Chroma
from app.rag.embedder import embedder

def get_vectorstore(persist_dir: str = "vectorstore"):
    return Chroma(collection_name="bc_assistant",
                  embedding_function=embedder(),
                  persist_directory=persist_dir)
