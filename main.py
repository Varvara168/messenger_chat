from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Убедитесь, что импорты правильные
from back.routers.auth import router as auth_router
from back.routers.chats import router as chats_router
from back.routers.messages import router as messages_router
from back.routers.search_user import router as search_user_router
from back.routers.status import router as status_router

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://87.228.36.68", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(messages_router)
app.include_router(search_user_router)
app.include_router(status_router)


app.mount("/static", StaticFiles(directory="front"), name="static")

@app.get("/")
def serve_login():
    return FileResponse("front/login.html")

@app.get("/chat")
def serve_chat():
    return FileResponse("front/chat.html")

@app.get("/register")
def serve_register():
    return FileResponse("front/register.html")

