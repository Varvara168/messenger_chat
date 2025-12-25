from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from db import get_db
from back.models.messages import Message
from back.models.users import User
from back.models.chats import Chat
from back.schemas.messages import MessageCreate, MessageOut, SenderOut
from back.get_current_user import get_current_user
from back.models.chat_members import ChatMembers


router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/by_user", response_model=MessageOut)
def send_message_to_user(
    message_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ID_QUERY теперь это ID чата
    chat_id = int(message_in.id_query)
    
    # Проверяем, существует ли чат и является ли текущий пользователь его участником
    chat = db.execute(
        select(Chat)
        .join(ChatMembers, Chat.id == ChatMembers.chat_id)
        .where(
            Chat.id == chat_id,
            ChatMembers.user_id == current_user.id
        )
    ).scalar_one_or_none()

    if not chat:
        raise HTTPException(404, "Chat not found or you are not a member")
    
    # Проверяем, что чат персональный (если нужно)
    if chat.type != "personal":
        raise HTTPException(400, "Can only send messages to personal chats")
    
    # Получаем второго участника чата (получателя сообщения)
    other_member = db.execute(
        select(User)
        .join(ChatMembers, User.id == ChatMembers.user_id)
        .where(
            ChatMembers.chat_id == chat_id,
            User.id != current_user.id  # Исключаем отправителя
        )
    ).scalar_one_or_none()

    if not other_member:
        raise HTTPException(404, "Receiver not found in chat")
    
    # Проверяем, не пишем ли мы сами себе
    if other_member.id == current_user.id:
        raise HTTPException(400, "Cannot send message to yourself")
    
    # Создаем сообщение
    message = Message(
        chat_id=chat_id,
        user_id=current_user.id,
        text=message_in.content,
        photo_url="",
        attachments="",
        timestamp=datetime.utcnow(),
        status="sent"
    )
    
    db.add(message)
    
    # Обновляем последнее сообщение в чате
    chat.last_message = message_in.content
    db.commit()
    db.refresh(message)
    
    # Формируем ответ
    return MessageOut(
        sender=SenderOut(
            id=current_user.id,
            short_name=current_user.short_name,
            avatar=current_user.avatar
        ),
        message=message.text,
        timestamp=message.timestamp
    )