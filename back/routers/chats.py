from fastapi import APIRouter, HTTPException, Response, Depends, Query
from sqlalchemy import select, or_, desc, delete
from sqlalchemy.orm import Session

from db import get_db
from back.models.chats import Chat
from back.schemas.chats import ChatCreate, ChatOut
from back.models.users import User
from back.routers.auth import security
from back.models.messages import Message
from back.schemas.messages import MessageOut, MessagesResponse
from back.models.chat_members import ChatMembers
from back.schemas.messages import SenderOut
from datetime import datetime


router = APIRouter(prefix="/chat", tags=["chat"])

def get_current_user(db: Session = Depends(get_db)) -> User:
    # текущий пользователь фиксирован
    user = db.execute(select(User).where(User.short_name == "maksim_dyakov")).scalar_one_or_none()
    if not user:
        raise HTTPException(401, "User not found")
    return user


@router.post("/create_chat")
def create_chat(chat: ChatCreate, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    
    chat_member = db.execute(
        select(User)
        .where(or_(User.short_name == chat.query, User.phone == chat.query))
    ).scalar_one_or_none()
    
    if not chat_member:
        raise HTTPException(status_code=404, detail="User not found") #Такой пользователь не найден
    
    if chat_member.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot create chat with yourself") #Нельзя создать чат с самим собой

    # Проверяем, есть ли уже личный чат с этим пользователем
    existing_chat = db.execute(
        select(Chat)
        .join(ChatMembers)
        .where(
            Chat.type == "personal",
            ChatMembers.user_id.in_([current_user.id, chat_member.id])
        )
    ).scalars().all()

    # Если чат уже есть с этими двумя пользователями — возвращаем его
    for c in existing_chat:
        member_ids = [m.user_id for m in db.execute(select(ChatMembers).where(ChatMembers.chat_id == c.id)).scalars().all()]
        if set(member_ids) == set([current_user.id, chat_member.id]):
            return c
    
    new_chat = Chat(
        type="personal",
        title=chat_member.first_name,
        members=", ".join([str(current_user.id), str(chat_member.id)]),
        last_message=None
    )

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    db.add_all([
        ChatMembers(chat_id=new_chat.id, user_id=current_user.id),
        ChatMembers(chat_id=new_chat.id, user_id=chat_member.id)
    ])

    db.commit()
    db.refresh(new_chat)

    return new_chat #Чат успешно создан



@router.get("/get_chats", response_model=list[ChatOut])
def get_chats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Получаем все чаты пользователя
    chat_ids = db.execute(
        select(ChatMembers.chat_id)
        .where(ChatMembers.user_id == current_user.id)
    ).scalars().all()

    chats = db.execute(select(Chat).where(Chat.id.in_(chat_ids))).scalars().all()
    result = []

    for chat in chats:
        # Получаем всех участников кроме текущего пользователя
        members = db.execute(
            select(User).join(ChatMembers).where(ChatMembers.chat_id == chat.id, User.id != current_user.id)
        ).scalars().all()

        chat_title = ", ".join(u.first_name for u in members)
        all_members = db.execute(
            select(User).join(ChatMembers).where(ChatMembers.chat_id == chat.id)
        ).scalars().all()

        last_message = db.execute(
            select(Message)
            .where(Message.chat_id == chat.id)
            .order_by(desc(Message.timestamp))
            .limit(1)
        ).scalar_one_or_none()

        result.append(ChatOut(
            id=chat.id,
            type=chat.type,
            title=chat_title or chat.title,
            members=",".join(str(u.id) for u in all_members),
            last_message=last_message.text if last_message else None
        ))

    return result


@router.get("/{id}/messages", response_model=MessagesResponse)
def get_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    chat = db.get(Chat, chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")

    # 1️⃣ проверка участия в чате
    member_ids = db.execute(
        select(ChatMembers.user_id)
        .where(ChatMembers.chat_id == chat_id)
    ).scalars().all()

    if current_user.id not in member_ids:
        raise HTTPException(403, "Not a member of this chat")

    # 2️⃣ получаем сообщения
    messages = db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.timestamp)
        .limit(limit)
        .offset(offset)
    ).scalars().all()

    now = datetime.utcnow()

    # 3️⃣ delivered_at — пользователь ПОЛУЧИЛ сообщения
    undelivered = db.execute(
        select(Message)
        .where(
            Message.chat_id == chat_id,
            Message.user_id != current_user.id,
            Message.delivered_at.is_(None)
        )
    ).scalars().all()

    for m in undelivered:
        m.delivered_at = now

    # 4️⃣ read_at — пользователь ПРОЧИТАЛ чат
    unread = db.execute(
        select(Message)
        .where(
            Message.chat_id == chat_id,
            Message.user_id != current_user.id,
            Message.read_at.is_(None)
        )
    ).scalars().all()

    for m in unread:
        m.read_at = now

    db.commit()

    # 5️⃣ формируем ответ
    result = []
    for m in messages:
        sender = m.sender
        result.append(
            MessageOut(
                sender=SenderOut(
                    id=sender.id,
                    short_name=sender.short_name,
                    avatar=sender.avatar
                ),
                message=m.text,
                timestamp=m.timestamp,
                delivered_at=m.delivered_at,
                read_at=m.read_at
            )
        )

    return {
        "chat_id": chat_id,
        "messages": result
    }

#просто удалить если модельки меняются 
@router.delete("/delete_personal_chats")
def delete_personal_chats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # находим все личные чаты пользователя
    chat_ids = db.execute(
        select(Chat.id)
        .join(ChatMembers)
        .where(ChatMembers.user_id == current_user.id, Chat.type == "personal")
    ).scalars().all()

    if chat_ids:
        db.execute(delete(ChatMembers).where(ChatMembers.chat_id.in_(chat_ids)))
        db.execute(delete(Chat).where(Chat.id.in_(chat_ids)))
        db.commit()

    return {"deleted_chats": len(chat_ids)}
