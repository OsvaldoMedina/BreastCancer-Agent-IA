# app/server.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.chains.assistant import chat
from app.security.auth import require_api_key

app = FastAPI(title="Breast Cancer Assistant", version="0.2.0")

class ChatIn(BaseModel):
    text: str

class ChatOut(BaseModel):
    content: str
    tool_used: str | None = None

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatOut)
async def chat_ep(body: ChatIn, _=Depends(require_api_key)):
    res = chat(body.text)
    return ChatOut(**res)
