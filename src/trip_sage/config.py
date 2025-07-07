import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv, find_dotenv


@dataclass(frozen=True)
class OpenAIAPIConfig:
    key: str
    model: str = "gpt-3.5-turbo-1106"
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> "OpenAIAPIConfig":
        return cls(
            key=os.environ["OPENAI_API_KEY"],
            model=os.environ.get("OPENAI_API_MODEL", "gpt-3.5-turbo-1106"),
            max_retries=int(os.environ.get("OPENAI_API_MAX_RETRIES", 3)),
        )


@dataclass(frozen=True, slots=True)
class SqliteConfig:
    path: str | Path = "./app.db"

    @property
    def url(self) -> str:
        file_path = Path(self.path).expanduser().resolve()
        return f"sqlite+aiosqlite:///{file_path}"


@dataclass(frozen=True)
class Config:
    db: SqliteConfig
    openai_config: OpenAIAPIConfig


def load_config() -> Config:
    load_dotenv(find_dotenv())

    db = SqliteConfig()
    openai = OpenAIAPIConfig.from_env()

    return Config(db=db, openai_config=openai)
