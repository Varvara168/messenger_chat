from pydantic import BaseModel
from typing import Optional

class ChatCreate(BaseModel):
    query: str


class ChatOut(BaseModel):
    id: int
    type: str   
    title: str
    members: str
    last_message: Optional[str] = None

    class Config:
        orm_mode = True #Позволяет работать с ORM моделями напрямую