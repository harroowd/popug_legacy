from async_generator import asynccontextmanager
from config.settings import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base

base_url = settings.database.database_url

engine = create_async_engine(base_url)

SessionLocal = async_sessionmaker(
    autoflush=False, bind=engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


@asynccontextmanager
async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
