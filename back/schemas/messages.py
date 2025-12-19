from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import relationship



class MessageCreate(BaseModel):
    receiver_query: str
    content: str

class SenderOut(BaseModel):
    id: int
    short_name: str
    avatar: str | None = None

class MessageOut(BaseModel):
    sender: SenderOut
    message: str
    timestamp: datetime
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
    
class MessagesResponse(BaseModel):
    chat_id: int
    messages: List[MessageOut]