from fastapi import APIRouter, HTTPException, Response, Depends
from db import get_db
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from back.schemas.users import UserLogin, UserRegister
from back.models.users import User
from back.utils.hashing import hash_password, verify_password
from back.config import config, security
from back.get_current_user import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user: UserRegister, db=Depends(get_db)):

    existing_user = db.execute(select(User).where(User.phone == user.phone)).scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this phone already exists") #Пользователь уже существует

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        short_name=user.short_name,
        password=hash_password(user.password),
        phone=user.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"} #Вы успешно зарегистрированы


@router.post("/login")
def login(creds: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.execute(
        select(User).where(
            or_(User.phone == creds.creds, User.short_name == creds.creds)
        )
    ).scalar_one_or_none()

    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(
            status_code=401, 
            detail="Invalid credentials"
        )
    
    # Создаем токен
    token = security.create_access_token(uid=str(user.id))
    
    # Устанавливаем куку с длительным сроком
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        max_age=86400  # 24 часа в секундах
    )
    
    return {
        "message": "Login successful",
        "access_token": token, 
        "user_id": str(user.id),
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "short_name": user.short_name,
            "phone": user.phone
        }
    }

@router.post("/logout")
def logout(response: Response):
    # Удаляем куку
    response.delete_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        path="/"
    )
    return {"message": "Logged out successfully"}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "message": "Welcome to the main window!",
        "user": {
            "id": current_user.id,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "short_name": current_user.short_name,
            "phone": current_user.phone
        }
    }

