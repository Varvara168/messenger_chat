from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_query: str
    content: str

class MessageOut(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    timestamp: datetime
    status: str

    class Config:
        orm_mode = True
