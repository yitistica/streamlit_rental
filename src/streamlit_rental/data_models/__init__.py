from streamlit_rental.data_models.models import Customer
from streamlit_rental.data_models.declarative import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_sqlite_engine(db_path, echo=True):
    engine = create_engine(f'sqlite:///{db_path}', echo=echo)
    return engine


def create_tables(engine):
    Base.metadata.create_all(bind=engine)


def create_Session(db_path, echo=True):
    engine = create_sqlite_engine(db_path=db_path, echo=echo)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session
