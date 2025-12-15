from pydantic import BaseModel


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    short_name: str
    password: str
    phone: str
    avatar: str

class UserLogin(BaseModel):
    phone: str
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    short_name: str
    phone: str
    avatar: str

    class Config:
        from_attributes = True
