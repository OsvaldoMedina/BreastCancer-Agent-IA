# app/rag/embedder.py
from langchain_openai import OpenAIEmbeddings
from app.config import settings

def embedder():
    return OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY)
