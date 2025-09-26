import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session


def get_session() -> Session:
    session_factory = sessionmaker(
        bind=create_engine(
            url=URL.create(
                drivername="postgresql+psycopg",
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                username=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME"),
            ),
            echo=True if os.getenv("DB_ECHO") == "True" else False,
        )
    )
    return session_factory()
