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
    users = db.execute(
        select(User)
        .where(or_(
            User.short_name.ilike(f"%{query}%"),
            User.phone.ilike(f"%{query}%")
        ))
        .limit(20)
    ).scalars().all()

    return [UserOut.from_orm(user) for user in users]