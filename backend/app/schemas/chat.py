from datetime import datetime
from pydantic import BaseModel


class ChatRequest(BaseModel):
    profile_id: int
    conversation_id: int | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    user_message_id: int
    assistant_message_id: int
    reply: str
    replied_at: datetime