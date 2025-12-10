from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(url="sqlite:///clients.db")

session = sessionmaker(engine)

class Base(DeclarativeBase): #родительский класс
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    short_name: Mapped[str] = mapped_column(index=True) #очень быстрый поиск
    phone: Mapped[str]
    status: Mapped[str]
    message: Mapped[str]
    private_settings: Mapped[str]
    subscriptions: Mapped[str]  
    avatar: Mapped[str]

class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    title: Mapped[str]
    short_name: Mapped[str] = mapped_column(index=True)
    members: Mapped[str]
    last_message: Mapped[str]
    created_at: Mapped[str]

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    user_id: Mapped[int]
    text: Mapped[str]
    photo_url: Mapped[str]
    attachments: Mapped[str]
    timestamp: Mapped[str]
    status: Mapped[str]

class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int]
    privacy: Mapped[str]
    posts: Mapped[str]

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    members: Mapped[str]
    invites: Mapped[str]


# Создание таблиц
# Пользователь (User)

# — id
# — username
# — phone (опционально)
# — display_name
# — avatar
# — status ("online", "typing", "offline")
# — private_settings
# — subscriptions (каналы)

# Чат (Chat)

# — id
# — type (private / group)
# — title
# — short_name (для групп)
# — members[]
# — last_message
# — created_at

# Сообщение (Message)

# — id
# — chat_id
# — user_id
# — text
# — photo_url
# — attachments
# — timestamp
# — status (sent/read/delivered)

# Канал (Channel)

# — id
# — title
# — author_id
# — private/public
# — posts[]

# Группы (Group)

# — id
# — name
# — members[]
# — invites[]