from pydantic import BaseModel, Field


class RealtimePushTestRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class RealtimePushTestData(BaseModel):
    event: str
    content: str
    delivered_connection_count: int