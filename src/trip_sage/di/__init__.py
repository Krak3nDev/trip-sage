from dishka.integrations.fastapi import FastapiProvider

from .providers import (
    ConfigProvider,
    DbProvider,
    InfrastructureProvider,
    ServiceProvider,
)

providers = [
    FastapiProvider(),
    ConfigProvider(),
    DbProvider(),
    ServiceProvider(),
    InfrastructureProvider(),
]
