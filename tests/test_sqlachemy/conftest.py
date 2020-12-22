import pathlib

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from sqlalchemy import Column, String, Float, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database, create_database, database_exists

from . import Potato, PotatoCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)

    create_database(SQLALCHEMY_DATABASE_URL)

    yield


# noinspection PyPep8Naming
@pytest.fixture
def client():
    app = FastAPI()

    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def session():
        session = SessionLocal()
        try:
            yield session
            session.commit()
        finally:
            session.close()

    class PotatoModel(Base):
        __tablename__= 'potatoes'
        id = Column(Integer, primary_key=True, index=True)
        thickness = Column(Float)
        mass = Column(Float)
        color = Column(String)
        type = Column(String)

    Base.metadata.create_all(bind=engine)

    app.include_router(SQLAlchemyCRUDRouter(model=Potato, db_model=PotatoModel, db=session, create_schema=PotatoCreate))

    yield TestClient(app)




