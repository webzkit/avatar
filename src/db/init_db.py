from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from .session import engine


def init_database():
    if not database_exists(engine.url):
        create_database(engine.url)
        print("New Database Created")
        print(database_exists(engine.url))
    else:
        print("Database Already Exists")


def init_data_database(db: Session) -> None:
    # Tables drop all before create
    # Base.metadata.drop_all(bind=engine)

    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    pass
