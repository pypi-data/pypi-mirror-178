from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from gww_service.config import settings

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    settings.postgres_user,
    settings.postgres_password,
    settings.postgres_host,
    settings.postgres_database
)

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
