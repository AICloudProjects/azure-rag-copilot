#app/api.py

from fastapi import APIRouter
import uuid
from app.schemas import ChatRequest, ChatResponse, Usage
from app.services.rag import answer_question

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    rid = str(uuid.uuid4())

    user_msg = req.messages[-1].content

    # Clean high-level call
    output, usage_raw = answer_question(user_msg)

    usage = Usage(
        prompt_tokens=usage_raw.prompt_tokens,
        completion_tokens=usage_raw.completion_tokens,
        total_tokens=usage_raw.total_tokens
    )

    return ChatResponse(
        request_id=rid,
        output=output,
        usage=usage
    )

