from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db import Base



class ChatMembers(Base):
    __tablename__ = "chat_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
