from fastapi import FastAPI
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from fastapi_crudrouter import SQLAlchemyCRUDRouter
from tests import (
    Carrot,
    CarrotCreate,
    CarrotUpdate,
    CustomPotato,
    PAGINATION_SIZE,
    Potato,
    PotatoType,
    CUSTOM_TAGS,
    config,
)

DSN_LIST = [
    "sqlite:///./test.db?check_same_thread=false",
    # config.MSSQL_URI,
    config.POSTGRES_URI,
]


def _setup_base_app(db_uri: str = DSN_LIST[0]):
    if database_exists(db_uri):
        drop_database(db_uri)

    create_database(db_uri)

    app = FastAPI()

    engine = create_engine(db_uri)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def session():
        session = SessionLocal()
        try:
            yield session
            session.commit()
        finally:
            session.close()

    return app, engine, Base, session


def sqlalchemy_implementation(db_uri: str):
    app, engine, Base, session = _setup_base_app(db_uri)

    class PotatoModel(Base):
        __tablename__ = "potatoes"
        id = Column(Integer, primary_key=True, index=True)
        thickness = Column(Float)
        mass = Column(Float)
        color = Column(String)
        type = Column(String)

    class CarrotModel(Base):
        __tablename__ = "carrots"
        id = Column(Integer, primary_key=True, index=True)
        length = Column(Float)
        color = Column(String)

    Base.metadata.create_all(bind=engine)
    router_settings = [
        dict(
            schema=Potato,
            db_model=PotatoModel,
            db=session,
            prefix="potato",
            paginate=PAGINATION_SIZE,
        ),
        dict(
            schema=Carrot,
            db_model=CarrotModel,
            db=session,
            create_schema=CarrotCreate,
            update_schema=CarrotUpdate,
            prefix="carrot",
            tags=CUSTOM_TAGS,
        ),
    ]

    return app, SQLAlchemyCRUDRouter, router_settings


# noinspection DuplicatedCode
def sqlalchemy_implementation_custom_ids():
    app, engine, Base, session = _setup_base_app()

    class PotatoModel(Base):
        __tablename__ = "potatoes"
        potato_id = Column(Integer, primary_key=True, index=True)
        thickness = Column(Float)
        mass = Column(Float)
        color = Column(String)
        type = Column(String)

    Base.metadata.create_all(bind=engine)
    app.include_router(
        SQLAlchemyCRUDRouter(schema=CustomPotato, db_model=PotatoModel, db=session)
    )

    return app


def sqlalchemy_implementation_string_pk():
    app, engine, Base, session = _setup_base_app()

    class PotatoTypeModel(Base):
        __tablename__ = "potato_type"
        name = Column(String, primary_key=True, index=True)
        origin = Column(String)

    Base.metadata.create_all(bind=engine)
    app.include_router(
        SQLAlchemyCRUDRouter(
            schema=PotatoType,
            create_schema=PotatoType,
            db_model=PotatoTypeModel,
            db=session,
            prefix="potato_type",
        )
    )

    return app


def sqlalchemy_implementation_integrity_errors():
    app, engine, Base, session = _setup_base_app()

    class PotatoModel(Base):
        __tablename__ = "potatoes"
        id = Column(Integer, primary_key=True, index=True)
        thickness = Column(Float)
        mass = Column(Float)
        color = Column(String, unique=True)
        type = Column(String)

    class CarrotModel(Base):
        __tablename__ = "carrots"
        id = Column(Integer, primary_key=True, index=True)
        length = Column(Float)
        color = Column(String)

    Base.metadata.create_all(bind=engine)
    app.include_router(
        SQLAlchemyCRUDRouter(
            schema=Potato,
            db_model=PotatoModel,
            db=session,
            create_schema=Potato,
            prefix="potatoes",
        )
    )
    app.include_router(
        SQLAlchemyCRUDRouter(
            schema=Carrot,
            db_model=CarrotModel,
            db=session,
            update_schema=CarrotUpdate,
            prefix="carrots",
        )
    )

    return app
