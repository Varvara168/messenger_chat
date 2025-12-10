from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# чтобы фронт с другого порта мог обращаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или свой фронт: "http://localhost:5500"
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}
