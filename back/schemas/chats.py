from pydantic import BaseModel
from typing import Optional

class ChatCreate(BaseModel):
    creds: str


class ChatOut(BaseModel):
    id: int
    type: str   
    title: str
    members: str
    last_message: Optional[str] = None

    model_config = {
        "from_attributes": True
    }