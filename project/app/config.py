import logging
import os
from functools import lru_cache
from typing import Optional, Dict, Any
from pydantic import BaseSettings, AnyUrl, validator
import enum
import platform

import pydantic

logger = logging.getLogger(__name__)


class ExecutionType(str, enum.Enum):
    LOCAL = "LOCAL"
    DOCKER_LOCAL = "DOCKER_LOCAL"
    DOCKER_TEST = "DOCKER_TEST"
    AWS_DEVELOPMENT = "AWS_DEVELOP"
    AWS_PROD = "AWS_PROD"


class Settings(BaseSettings):
    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    # Environment
    API_V1_STR: str = "/prod/v1"
    ENVIRONMENT: str = "dev"
    TESTING: bool = 0

    # Database
    DATABASE_HOSTNAME: Optional[str] = None
    DATABASE_PORT: int = 5432
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_NAME: Optional[str] = None
    DATABASE_USERNAME: Optional[str] = None
    DATABASE_URL: Optional[AnyUrl] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        assert isinstance(
            values.get("DATABASE_HOSTNAME"), str
        ), "Couldn't figure out the Database URL"
        DATABASE_URL_FORMATTER = "postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
        return DATABASE_URL_FORMATTER.format(
            DATABASE_USERNAME=values.get("DATABASE_USERNAME"),
            DATABASE_PASSWORD=values.get("DATABASE_PASSWORD"),
            DATABASE_HOSTNAME=values.get("DATABASE_HOSTNAME"),
            DATABASE_PORT=values.get("DATABASE_PORT"),
            DATABASE_NAME=values.get("DATABASE_NAME"),
        )

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "app"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "app": {"handlers": ["default"], "level": LOG_LEVEL},
    }


# Usage
# from logging.config import dictConfig
# import logging
# from .config import LogConfig
#
# dictConfig(LogConfig().dict())
# logger = logging.getLogger("mycoolapp")
#
# logger.info("Dummy Info")
# logger.error("Dummy Error")
# logger.debug("Dummy Debug")
# logger.warning("Dummy Warning")


def validate_and_change_directory():
    logger.info("Loading config settings from the environment...")
    last_base_name = os.path.basename(os.path.normpath(os.getcwd()))
    if last_base_name != "project":
        logger.warning("Changing working directory")
        if last_base_name == "prod-backend":
            os.chdir(os.path.join(os.getcwd(), "project"))
        else:
            logger.warning("Couldn't change working directory")


@lru_cache()
def get_settings(env_file: Optional[str] = None) -> Settings:
    validate_and_change_directory()
    if env_file is None:
        env_file = os.environ.get("ENV_FILE", ".env.local")
    assert os.path.exists(
        env_file
    ), f"Env file: {env_file} was not found in {os.getcwd()}"
    return Settings(_env_file=env_file)

# FIXME: ¿Why is it an exact path?
if __name__ == "__main__":
    settings = Settings(
        _env_file="C:\\Users\\usuario\\Desktop\\Camilo\\ERP\\erpdev-backend\\project\\.env.local"
    )
    print(settings)
