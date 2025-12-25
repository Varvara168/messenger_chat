from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# правильная строка подключения
engine = create_engine(
    "postgresql+psycopg2://messenger_user:password@localhost:5432/messenger_db",
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