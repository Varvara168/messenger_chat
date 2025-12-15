from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy import select, or_, desc
from sqlalchemy.orm import Session

from db import get_db
from back.models.chats import Chat
from back.schemas.chats import ChatCreate, ChatOut
from back.models.users import User
from back.routers.auth import security
from back.models.messages import Message

router = APIRouter(prefix="/chat", tags=["chat"])

def get_current_user(db: Session = Depends(get_db)) -> User:
    user = db.execute(
        select(User).where(User.short_name == "maksim_dyakov")
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(401, "User not found")

    return user

@router.post("/create_chat")
def create_chat(chat: ChatCreate, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    
    chat_member = db.execute(select(User).where(or_(User.short_name == chat.query, User.phone == chat.query))).scalar_one_or_none()
    
    if not chat_member:
        raise HTTPException(status_code=404, detail="User not found") #Такой пользователь не найден
    
    if chat_member.short_name == current_user.short_name:
        raise HTTPException(status_code=400, detail="Cannot create chat with yourself") #Нельзя создать чат с самим собой

    members = ",".join(map(str, sorted([current_user.short_name, chat_member.short_name])))
    
    existing = db.execute(
        select(Chat).where(Chat.members == members)
    ).scalar_one_or_none()

    if existing:
        existing
    
    new_chat = Chat(
        type="personal",
        title=chat_member.first_name,
        members=members,
        last_message=None
    )

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat #Чат успешно создан


@router.get("/get_chats", response_model=list[ChatOut])
def get_chats(current_user: str, db=Depends(get_db)):
    # ищем пользователя
    user = db.execute(select(User).where(User.short_name == current_user)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # получаем все чаты, где участвует current_user
    chats = db.execute(select(Chat)).scalars().all()

    result = []
    for chat in chats:
        members_list = chat.members.split(",")
        if current_user not in members_list:
            continue

        other_members = [m for m in members_list if m != current_user]
        other_users = db.execute(select(User).where(User.short_name.in_(other_members))).scalars().all()
        chat_title = ", ".join([u.first_name for u in other_users])

        last_message = db.execute(
            select(Message)
            .where(Message.chat_id == chat.id)
            .order_by(desc(Message.timestamp))
            .limit(1)
        ).scalars().first()

        result.append(ChatOut(
            id=chat.id,
            type=chat.type,
            title=chat_title,
            members=chat.members,
            last_message=last_message.text if last_message else None
        ))
    return result 


