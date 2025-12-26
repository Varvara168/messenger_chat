from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from back.models.users import User
from back.schemas.users import UserOut
from db import get_db


router = APIRouter(prefix="/search", tags=["search"])

@router.get("/users", response_model=List[UserOut])
def search_users(query: str, db: Session = Depends(get_db)) -> List[UserOut]:
    if not query or not query.strip():
        return []
    
    search_term = f"%{query.strip()}%"
    
    # Ищем по отдельным полям
    users = db.execute(
        select(User)
        .where(or_(
            User.first_name.ilike(search_term),
            User.last_name.ilike(search_term),
            User.short_name.ilike(search_term),
            User.phone.ilike(search_term),
            # Ищем по комбинации "Имя Фамилия"
            (User.first_name + ' ' + User.last_name).ilike(search_term),
            # Ищем по комбинации "Фамилия Имя"
            (User.last_name + ' ' + User.first_name).ilike(search_term)
        ))
        .limit(20)
    ).scalars().all()

    return [UserOut.from_orm(user) for user in users]