from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from db import session, get_db
from sqlalchemy import select
from sqlalchemy.orm import Session

from back.schemas.users import UserLogin, UserRegister
from back.models.users import User
from back.utils.hashing import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


config = AuthXConfig()
config.JWT_SECRET_KEY = "your_secret_key" #секретный ключ для подписи JWT
config.JWT_ACCESS_COOKIE_NAME = "access_token" #имя куки для доступа
config.JWT_TOKEN_LOCATION = ["cookies"] #где хранить токен

security = AuthX(config=config)


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
        phone=user.phone,
        avatar=user.avatar
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"} #Вы успешно зарегистрированы


@router.post("/login")
def login(creds: UserLogin, response: Response, db: Session = Depends(get_db)):

    user = db.execute(select(User).where(User.phone == creds.phone)).scalar_one_or_none()

    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials") #Неверные учетные данные
    
    token = security.create_access_token(uid=str(user.id)) #создание токена для пользователя

    response.set_cookie( #установка куки с токеном
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,  # для безопасности
        secure=False     # На локальной разработке поставьте False
    )

    return {"access_token": token}


@router.get(path="/me", dependencies=[Depends(security.access_token_required)])
def me():
    if True:
        return {"message": "Welcome to the main window!"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
