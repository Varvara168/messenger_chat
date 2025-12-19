from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey 
from db import Base
from sqlalchemy.types import DateTime
from datetime import datetime




class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str]
    photo_url: Mapped[str]
    attachments: Mapped[str]
    timestamp: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(default="sent")  # sent, delivered, read
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    read_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)

    sender = relationship("User", lazy="joined")

    @property
    def content(self):
        return self.text
