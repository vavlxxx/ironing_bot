import os
from typing_extensions import Self
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def _get_env_var(env_var: str, to_cast: type) -> str:
    value = os.getenv(env_var)
    if value is None:
        raise ValueError(f'Environment variable {env_var} is not set')
    return to_cast(value)


@dataclass(frozen=True, repr=False, eq=False, slots=True)
class Settings:
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    DB_TABLE_ORDERS: str
    DB_TABLE_USERS: str

    BOT_TOKEN: str

    @classmethod
    def load_from_env(cls) -> Self:
        return cls(
            DB_USER=_get_env_var('DB_USER', to_cast=str),
            DB_PASS=_get_env_var('DB_PASS', to_cast=str),
            DB_HOST=_get_env_var('DB_HOST', to_cast=str),
            DB_PORT=_get_env_var('DB_PORT', to_cast=str),
            DB_NAME=_get_env_var('DB_NAME', to_cast=str),

            DB_TABLE_ORDERS=_get_env_var('DB_TABLE_ORDERS', to_cast=str),
            DB_TABLE_USERS=_get_env_var('DB_TABLE_USERS', to_cast=str),

            BOT_TOKEN=_get_env_var('BOT_TOKEN', to_cast=str),
        )
    
    @property
    def database_url(self) -> str:
        return (f'mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}'
                f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')


settings = Settings.load_from_env()
