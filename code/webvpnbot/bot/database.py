from sqlalchemy import (
    Column, Integer, String, DateTime, Index, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session as SyncSession
from datetime import datetime

Base = declarative_base()

# Настройки подключения к базе данных
DATABASE_URL_SYNC = "sqlite:///./database.db"  # Синхронный движок для Flask
DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./database.db"  # Асинхронный движок для бота

# Создание движков
sync_engine = create_engine(DATABASE_URL_SYNC, connect_args={"check_same_thread": False})
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)

# Фабрика асинхронных сессий (Telegram-бот)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Фабрика синхронных сессий (Flask)
SessionLocal = sessionmaker(
    bind=sync_engine,
    class_=SyncSession,
    expire_on_commit=False
)

class AuthorizedUser(Base):
    __tablename__ = 'authorized_users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)

class OTPSession(Base):
    __tablename__ = 'otp_sessions'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    otp = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

# Создаём индексы
Index('ix_otp_sessions_username', OTPSession.username)
Index('ix_authorized_users_telegram_id', AuthorizedUser.telegram_id)

# Функция для синхронного создания таблиц (Flask)
def init_db_sync():
    Base.metadata.create_all(sync_engine)

# Асинхронная функция для создания таблиц (бот)
async def init_db_async():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)