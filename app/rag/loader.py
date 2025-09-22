# app/rag/loader.py
from typing import List
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

SUPPORTED = {".pdf", ".txt", ".md"}

def load_documents(root: str) -> List:
    docs = []
    for p in Path(root).rglob("*"):
        if p.suffix.lower() not in SUPPORTED:
            continue
        if p.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(p))
            docs.extend(loader.load())
        else:
            loader = TextLoader(str(p), encoding="utf-8")
            docs.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    return splitter.split_documents(docs)
