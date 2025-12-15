from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from db import Base
from datetime import datetime

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    title: Mapped[str] = mapped_column(index=True) #берется из имени собеседника автооматически в личном чате 
    members: Mapped[str]
    last_message: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
