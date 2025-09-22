# scripts/index_knowledge.py
import argparse
from app.rag.loader import load_documents
from app.rag.vectorstore import get_vectorstore

def main(root: str, persist: str = "vectorstore"):
    docs = load_documents(root)
    vs = get_vectorstore(persist)
    vs.add_documents(docs)
    vs.persist()
    print(f"Indexados {len(docs)} chunks en {persist}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/knowledge")
    ap.add_argument("--persist", default="vectorstore")
    args = ap.parse_args()
    main(args.root, args.persist)
