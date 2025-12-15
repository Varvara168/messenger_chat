from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import engine, Base

from back.routers.auth import router as auth_router
from back.routers.chats import router as chats_router
from back.routers.messages import router as messages_router

Base.metadata.create_all(engine)

app = FastAPI()

# чтобы фронт с другого порта мог обращаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или свой фронт: "http://localhost:5500"
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(messages_router)

# venv\Scripts\activate    
# py -m uvicorn main:app --reload