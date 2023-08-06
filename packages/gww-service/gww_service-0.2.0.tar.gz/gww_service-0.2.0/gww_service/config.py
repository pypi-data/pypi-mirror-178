from os import getenv

from pydantic import BaseModel, BaseSettings

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "gww-service"
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
        "gww-service": {"handlers": ["default"], "level": LOG_LEVEL},
    }

class Settings(BaseSettings):
    postgres_user: str = getenv("PSQL_USER", "testuser")
    postgres_password: str = getenv("PSQL_PASSWORD", "testpassword")
    postgres_database: str = getenv("PSQL_DB", "testdb")
    postgres_host: str = getenv("PSQL_HOST", "localhost")
    use_ee: bool = bool(getenv("USE_EE"))

settings = Settings()
