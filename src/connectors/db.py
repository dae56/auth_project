import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session


def get_session() -> Session:
    engine = create_engine(
        url=URL.create(
            drivername='postgresql+psycopg2',
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            username=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        ),
        echo=os.getenv('DB_ECHO')
    )
    session_factory = sessionmaker(bind=engine)
    with session_factory() as session:
        yield session
