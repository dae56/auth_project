import os

from sqlalchemy import create_engine, URL, Engine
from sqlalchemy.orm import sessionmaker, Session

from src.models.db.user import User, RoleUser
from src.utils.auth import get_hash_data


def get_engine() -> Engine:
    return create_engine(
        url=URL.create(
            drivername="postgresql+psycopg",
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
        ),
        echo=True if os.getenv("DB_ECHO") == "True" else False
    )


def get_session() -> Session:
    session_factory = sessionmaker(bind=get_engine())
    with session_factory() as session:
        return session


def refresh_table() -> None:
    User.metadata.drop_all(bind=get_engine())
    User.metadata.create_all(bind=get_engine())
    session = get_session()
    session.add(
        User(
            first_name="superadmin",
            last_name="superadmin",
            email="superadmin@example.com",
            password_hash=get_hash_data(data="superadmin", salt=os.getenv("PASS_SALT")),
            role=RoleUser.admin
        )
    )
    session.commit()
