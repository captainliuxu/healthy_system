from datetime import datetime

from pydantic import BaseModel, Field

# 定义前端发消息时的请求体。
class ChatSendRequest(BaseModel):
    conversation_id: int = Field(..., ge=1)
    content: str = Field(..., min_length=1, max_length=2000)

# 定义后端回复给前端的数据结构。
class ChatSendData(BaseModel):
    conversation_id: int
    user_message_id: int
    assistant_message_id: int
    reply: str
    replied_at: datetime