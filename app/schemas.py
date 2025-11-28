# app/schemas.py
from pydantic import BaseModel
from typing import List, Literal

class Message(BaseModel):
    role: Literal["system","user","assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: float = 0.2

class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class ChatResponse(BaseModel):
    request_id: str
    output: str
    usage: Usage
