from dishka import AsyncContainer, make_async_container

from trip_sage.config import Config, OpenAIAPIConfig, SqliteConfig
from trip_sage.di import providers


def setup_ioc_container(
    config: Config,
) -> AsyncContainer:
    container = make_async_container(
        *providers,
        context={
            Config: config,
            SqliteConfig: config.db,
            OpenAIAPIConfig: config.openai_config,
        },
    )
    return container
