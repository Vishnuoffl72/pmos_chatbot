from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import get_response

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.post("/")
async def chat_endpoint(chat_input: ChatMessage):
    response_text = get_response(chat_input.message)
    return {"response": response_text}
