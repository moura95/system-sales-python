from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, \
    create_async_engine

from midas_sales.config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        async with session.begin():
            yield session
