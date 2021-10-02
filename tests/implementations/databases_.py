import databases
from fastapi import FastAPI
from sqlalchemy import Column, Float, Integer, MetaData, String, Table, create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from fastapi_crudrouter import DatabasesCRUDRouter
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


def _setup_database(db_uri: str = DSN_LIST[0]):
    if database_exists(db_uri):
        drop_database(db_uri)

    create_database(db_uri)
    database = databases.Database(db_uri)
    engine = create_engine(db_uri)

    return engine, database


def databases_implementation(db_uri: str):
    engine, database = _setup_database(db_uri)

    metadata = MetaData()
    potatoes = Table(
        "potatoes",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("thickness", Float),
        Column("mass", Float),
        Column("color", String),
        Column("type", String),
    )
    carrots = Table(
        "carrots",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("length", Float),
        Column("color", String),
    )
    metadata.create_all(bind=engine)

    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    router_settings = [
        dict(
            database=database,
            table=potatoes,
            schema=Potato,
            prefix="potato",
            paginate=PAGINATION_SIZE,
        ),
        dict(
            database=database,
            table=carrots,
            schema=Carrot,
            create_schema=CarrotCreate,
            update_schema=CarrotUpdate,
            prefix="carrot",
            tags=CUSTOM_TAGS,
        ),
    ]

    return app, DatabasesCRUDRouter, router_settings


def databases_implementation_custom_ids():
    engine, database = _setup_database()

    metadata = MetaData()
    potatoes = Table(
        "potatoes",
        metadata,
        Column("potato_id", Integer, primary_key=True),
        Column("thickness", Float),
        Column("mass", Float),
        Column("color", String),
        Column("type", String),
    )

    metadata.create_all(bind=engine)

    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    potato_router = DatabasesCRUDRouter(
        database=database, table=potatoes, schema=CustomPotato
    )
    app.include_router(potato_router)

    return app


def databases_implementation_string_pk():
    engine, database = _setup_database()

    metadata = MetaData()
    potato_types = Table(
        "potato_type",
        metadata,
        Column("name", String, primary_key=True),
        Column("origin", String),
    )

    metadata.create_all(bind=engine)

    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    potato_router = DatabasesCRUDRouter(
        database=database,
        table=potato_types,
        schema=PotatoType,
        create_schema=PotatoType,
    )
    app.include_router(potato_router)

    return app
