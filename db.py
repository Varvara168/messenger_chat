from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# правильная строка подключения
engine = create_engine(
    "postgresql://postgres:postgres@db:5432/messenger",
    echo=True
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass