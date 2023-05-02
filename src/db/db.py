from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.settings import settings

__all__ = ("base", "get_async_session")

base = declarative_base()

async_engine = create_async_engine(settings.db.url, future=True, echo=settings.db.echo)


async def get_async_session():
    async_session = sessionmaker(  # type: ignore
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with async_session() as session:
        yield session
