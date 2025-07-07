import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncContextManager, AsyncIterator, Callable

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from trip_sage.config import SqliteConfig, load_config
from trip_sage.di.setup import setup_ioc_container
from trip_sage.endpoints import recommendations_router
from trip_sage.exception_handlers import register_exception_handlers
from trip_sage.log import setup_logging
from trip_sage.persistence.models import Base


def db_startup_lifespan(
    container: AsyncContainer, db_config: SqliteConfig
) -> Callable[[FastAPI], AsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine: AsyncEngine = await container.get(AsyncEngine)

        db_path = Path(db_config.path).expanduser().resolve()
        need_migrations = not db_path.exists()

        if need_migrations:
            async with engine.begin() as conn:
                logging.error(Base.metadata.tables)
                await conn.run_sync(Base.metadata.create_all)

        yield

        await engine.dispose()
        await container.close()

    return lifespan


def create_app() -> FastAPI:
    cfg = load_config()
    container = setup_ioc_container(config=cfg)
    setup_logging()

    app = FastAPI(
        title="Travel Recommender API",
        lifespan=db_startup_lifespan(container=container, db_config=cfg.db),
    )

    register_exception_handlers(app=app)

    setup_dishka(container=container, app=app)
    app.include_router(recommendations_router)
    return app
