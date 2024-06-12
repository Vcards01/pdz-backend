from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./database/pdz_hub.db"


engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)

Base = declarative_base()


async def get_session() -> AsyncGenerator:
    """ "Retorna sessão do banco de dados"""
    session: AsyncSession = session_local()
    try:
        yield session

    finally:
        await session.close()
