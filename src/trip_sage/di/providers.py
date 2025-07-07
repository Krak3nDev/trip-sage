from typing import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from trip_sage.config import Config, OpenAIAPIConfig, SqliteConfig
from trip_sage.openai import OpenAIAdapter
from trip_sage.persistence.repositories import RecommendationRepository
from trip_sage.persistence.setup import create_engine, create_session_pool
from trip_sage.services.recommendation import RecommendationService


class ConfigProvider(Provider):
    config = from_context(Config, scope=Scope.APP)
    db_config = from_context(SqliteConfig, scope=Scope.APP)
    openai = provide(OpenAIAPIConfig, scope=Scope.APP)


class ServiceProvider(Provider):
    recommendation_service = provide(
        RecommendationService, scope=Scope.REQUEST
    )


class InfrastructureProvider(Provider):
    openai_adapter = provide(OpenAIAdapter, scope=Scope.APP)


class DbProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self, db_config: SqliteConfig) -> AsyncEngine:
        return create_engine(db_config)

    @provide(scope=Scope.APP)
    async def session_pool(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return create_session_pool(engine)

    @provide(scope=Scope.REQUEST)
    async def session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_factory() as session:
            yield session

    recommendation_repo = provide(
        RecommendationRepository, scope=Scope.REQUEST
    )
