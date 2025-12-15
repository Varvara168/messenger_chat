from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str] 
    short_name: Mapped[str] 
    password: Mapped[str]
    phone: Mapped[str] = mapped_column(index=True) #очень быстрый поиск
    # status: Mapped[str]
    # message: Mapped[str]
    # private_settings: Mapped[str]
    # subscriptions: Mapped[str]  
    avatar: Mapped[str]