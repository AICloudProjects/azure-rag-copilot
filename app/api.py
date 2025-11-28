# app/api.py
import uuid
from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse, Usage

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    rid = str(uuid.uuid4())
    output = f"(mock) You said: {req.messages[-1].content}"
    usage = Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15)
    return ChatResponse(request_id=rid, output=output, usage=usage)
