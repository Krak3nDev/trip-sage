from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from trip_sage.config import SqliteConfig


def create_engine(cfg: SqliteConfig) -> AsyncEngine:
    return create_async_engine(
        cfg.url,
        query_cache_size=1200,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
    )


def create_session_pool(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
