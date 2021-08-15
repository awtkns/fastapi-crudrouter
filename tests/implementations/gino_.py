import asyncio
from fastapi import FastAPI
from fastapi_crudrouter import GinoCRUDRouter
from gino.ext.starlette import Gino
from sqlalchemy_utils import create_database, database_exists, drop_database
from tests import (
    CUSTOM_TAGS,
    PAGINATION_SIZE,
    Carrot,
    CarrotCreate,
    CarrotUpdate,
    CustomPotato,
    Potato,
    PotatoType,
    config,
)


GINO_DATABASE_URL = config.POSTGRES_URI.replace("postgresql", "asyncpg")


async def migrate(db):
    async with db.with_bind(GINO_DATABASE_URL):
        await db.gino.create_all()


def _setup_base_app():
    if database_exists(config.POSTGRES_URI):
        drop_database(config.POSTGRES_URI)

    create_database(config.POSTGRES_URI)

    app = FastAPI()
    db = Gino(dsn=GINO_DATABASE_URL)
    db.init_app(app)
    return db, app


def gino_implementation(**kwargs):
    db, app = _setup_base_app()

    class PotatoModel(db.Model):
        __tablename__ = "potatoes"
        id = db.Column(db.Integer, primary_key=True, index=True)
        thickness = db.Column(db.Float)
        mass = db.Column(db.Float)
        color = db.Column(db.String)
        type = db.Column(db.String)

    class CarrotModel(db.Model):
        __tablename__ = "carrots"
        id = db.Column(db.Integer, primary_key=True, index=True)
        length = db.Column(db.Float)
        color = db.Column(db.String)

    asyncio.get_event_loop().run_until_complete(migrate(db))

    router_settings = [
        dict(
            schema=Potato,
            db_model=PotatoModel,
            db=db,
            prefix="potato",
            paginate=PAGINATION_SIZE,
        ),
        dict(
            schema=Carrot,
            db_model=CarrotModel,
            db=db,
            create_schema=CarrotCreate,
            update_schema=CarrotUpdate,
            prefix="carrot",
            tags=CUSTOM_TAGS,
        ),
    ]

    return app, GinoCRUDRouter, router_settings


# noinspection DuplicatedCode
def gino_implementation_custom_ids():
    db, app = _setup_base_app()

    class PotatoModel(db.Model):
        __tablename__ = "potatoes"
        potato_id = db.Column(db.Integer, primary_key=True, index=True)
        thickness = db.Column(db.Float)
        mass = db.Column(db.Float)
        color = db.Column(db.String)
        type = db.Column(db.String)

    asyncio.get_event_loop().run_until_complete(migrate(db))

    app.include_router(GinoCRUDRouter(schema=CustomPotato, db_model=PotatoModel, db=db))

    return app


def gino_implementation_string_pk():
    db, app = _setup_base_app()

    class PotatoTypeModel(db.Model):
        __tablename__ = "potato_type"
        name = db.Column(db.String, primary_key=True, index=True)
        origin = db.Column(db.String)

    asyncio.get_event_loop().run_until_complete(migrate(db))

    app.include_router(
        GinoCRUDRouter(
            schema=PotatoType,
            create_schema=PotatoType,
            db_model=PotatoTypeModel,
            db=db,
            prefix="potato_type",
        )
    )

    return app


def gino_implementation_integrity_errors():
    db, app = _setup_base_app()

    class PotatoModel(db.Model):
        __tablename__ = "potatoes"
        id = db.Column(db.Integer, primary_key=True, index=True)
        thickness = db.Column(db.Float)
        mass = db.Column(db.Float)
        color = db.Column(db.String, unique=True)
        type = db.Column(db.String)

    class CarrotModel(db.Model):
        __tablename__ = "carrots"
        id = db.Column(db.Integer, primary_key=True, index=True)
        length = db.Column(db.Float)
        color = db.Column(db.String)

    asyncio.get_event_loop().run_until_complete(migrate(db))

    app.include_router(
        GinoCRUDRouter(
            schema=Potato,
            db_model=PotatoModel,
            db=db,
            create_schema=Potato,
            prefix="potatoes",
        )
    )
    app.include_router(
        GinoCRUDRouter(
            schema=Carrot,
            db_model=CarrotModel,
            db=db,
            update_schema=CarrotUpdate,
            prefix="carrots",
        )
    )

    return app
