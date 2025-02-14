from sqlalchemy import Column, Integer, String, DateTime, Index, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session as SyncSession
from datetime import datetime

Base = declarative_base()

# Асинхронный движок (для Telegram-бота)
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Синхронный движок (для Flask-приложения)
SYNC_DATABASE_URL = "sqlite:///db.sqlite3"
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

# Фабрика **асинхронных** сессий (Telegram-бот)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Фабрика **синхронных** сессий (Flask)
SessionLocal = sessionmaker(
    bind=sync_engine,
    class_=SyncSession,
    expire_on_commit=False
)

class AuthorizedUser(Base):
    __tablename__ = "authorized_users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)

class OTPSession(Base):
    __tablename__ = 'otp_sessions'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    otp = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

# Создаём индексы
Index('ix_otp_sessions_username', OTPSession.username)
Index('ix_authorized_users_telegram_id', AuthorizedUser.telegram_id)

# Асинхронная функция для создания таблиц
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
