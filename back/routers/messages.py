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
from back.models.chat_members import ChatMembers


router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/by_user", response_model=MessageOut)
def send_message_to_user(
    message_in: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sender = current_user

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
     
    possible_chats = db.execute(
        select(Chat)
        .join(ChatMembers)
        .where(Chat.type == "personal")
    ).scalars().all()

    chat = None
    for c in possible_chats:
        member_ids = [m.user_id for m in db.execute(select(ChatMembers).where(ChatMembers.chat_id == c.id)).scalars().all()]
        if set(member_ids) == set([sender.id, receiver.id]):
            chat = c
            break


    if not chat:
        chat = Chat(
            type="personal",
            title=receiver.first_name, 
            members=", ".join([str(current_user.id), str(receiver.id)]),
            last_message=None
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)
        db.add_all([
            ChatMembers(chat_id=chat.id, user_id=sender.id),
            ChatMembers(chat_id=chat.id, user_id=receiver.id)
        ])
        db.commit()


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

    # обновляем
    chat.last_message = message.text
    db.commit()

    return MessageOut.from_orm(message)



