# app/tools/search_knowledge.py
from typing import Dict, Any, List
import pathlib

def tool_spec() -> Dict[str, Any]:
    return {
        "name": "local_search",
        "description": "Busca fragmentos en documentos locales de /data/knowledge (RAG-lite).",
        "schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    }

def run(query: str, root: str = "data/knowledge", max_docs: int = 3) -> List[Dict[str, Any]]:
    q = query.lower().strip()
    rootp = pathlib.Path(root)
    hits = []
    for p in rootp.rglob("*.*"):
        if p.suffix.lower() in {".txt", ".md"}:
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            if q in text.lower():
                snippet = text.lower().split(q, 1)[-1][:500]
                hits.append({"path": str(p), "snippet": snippet})
                if len(hits) >= max_docs:
                    break
    return hits
