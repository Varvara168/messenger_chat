from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from datetime import datetime

from db import get_db
from back.models.messages import Message
from back.models.users import User
from back.models.chats import Chat
from back.schemas.messages import MessageCreate, MessageOut
from back.routers.chats import get_current_user

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/by_user", response_model=MessageOut)
def send_message_to_user(
    message_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sender = current_user

    # Находим получателя
    receiver = db.execute(
        select(User).where(
            or_(User.short_name == message_in.receiver_query,
                User.phone == message_in.receiver_query)
        )
    ).scalar_one_or_none()

    if not receiver:
        raise HTTPException(404, "Receiver not found")
    if receiver.id == sender.id:
        raise HTTPException(400, "Cannot send message to yourself")

    # Находим чат между ними
    members_sorted = sorted([sender.short_name, receiver.short_name])
    members_str = ",".join(members_sorted)

    chat = db.execute(select(Chat).where(Chat.members == members_str)).scalar_one_or_none()

    # Если чата нет — создаем
    if not chat:
        chat = Chat(
            type="personal",
            title=receiver.first_name,  # в title имя собеседника
            members=members_str
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)

    # Создаем сообщение
    message = Message(
        chat_id=chat.id,
        user_id=sender.id,
        text=message_in.content,
        photo_url="",
        attachments="",
        timestamp=datetime.utcnow(),
        status="sent"
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # Возвращаем через Pydantic
    return MessageOut(
        id=message.id,
        chat_id=message.chat_id,
        sender_id=message.user_id,
        content=message.text,
        timestamp=message.timestamp,
        status=message.status
    )
