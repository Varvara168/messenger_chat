from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(url="sqlite:///clients.db")

session = sessionmaker(engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close() 
        
class Base(DeclarativeBase): #родительский класс
    pass

# class Channel(Base):
#     __tablename__ = "channels"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str]
#     author_id: Mapped[int]
#     privacy: Mapped[str]
#     posts: Mapped[str]

# class Group(Base):
#     __tablename__ = "groups"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     members: Mapped[str]
#     invites: Mapped[str]