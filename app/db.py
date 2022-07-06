from .config import settings

from sqlmodel import create_engine, SQLModel, Session

engine = create_engine(settings.db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session