from fastapi import Depends, HTTPException, Request
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from back.models.users import User
from db import get_db
from back.config import config


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    # Пытаемся получить токен из куки
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    
    if not token:
        # Пробуем заголовок
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Декодируем токен
        payload = jwt.decode(
            token, 
            config.JWT_SECRET_KEY, 
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Ищем пользователя
        user = db.execute(
            select(User).where(User.id == int(user_id))
        ).scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")