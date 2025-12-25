from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    short_name: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column(index=True, unique=True) #очень быстрый поиск
    # status: Mapped[str]
    # message: Mapped[str]
    # private_settings: Mapped[str]
    # subscriptions: Mapped[str]  
    avatar: Mapped[str] = mapped_column(nullable=True)  # путь к аватарке