from sqlalchemy import text
from db import engine

with engine.connect() as conn:
    # добавляем новые колонки, если их нет
    try:
        conn.execute(text("ALTER TABLE messages ADD COLUMN delivered_at DATETIME"))
    except Exception:
        print("delivered_at уже существует или ошибка")
    try:
        conn.execute(text("ALTER TABLE messages ADD COLUMN read_at DATETIME"))
    except Exception:
        print("read_at уже существует или ошибка")
    conn.commit()
