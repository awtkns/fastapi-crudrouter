from fastapi import FastAPI
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database, create_database, database_exists

from fastapi_crudrouter import SQLAlchemyCRUDRouter
from tests import Potato, PotatoCreate, Carrot, CarrotCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


def sqlalchemy_implementation():
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)

    create_database(SQLALCHEMY_DATABASE_URL)

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
        __tablename__ = 'potatoes'
        id = Column(Integer, primary_key=True, index=True)
        thickness = Column(Float)
        mass = Column(Float)
        color = Column(String)
        type = Column(String)

    class CarrotModel(Base):
        __tablename__ = 'carrots'
        id = Column(Integer, primary_key=True, index=True)
        length = Column(Float)
        color = Column(String)

    Base.metadata.create_all(bind=engine)

    app.include_router(SQLAlchemyCRUDRouter(model=Potato, db_model=PotatoModel, db=session, create_schema=PotatoCreate))
    app.include_router(SQLAlchemyCRUDRouter(model=Carrot, db_model=CarrotModel, db=session, create_schema=CarrotCreate))

    return app

