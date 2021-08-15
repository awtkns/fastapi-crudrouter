import os

import databases
import ormar
import pytest
import sqlalchemy
from fastapi import FastAPI

from fastapi_crudrouter import OrmarCRUDRouter
from tests import CarrotCreate, CarrotUpdate, PAGINATION_SIZE, CUSTOM_TAGS

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


@pytest.fixture(scope="function", autouse=True)
async def cleanup():
    async with database:
        await PotatoModel.objects.delete(each=True)
        await CarrotModel.objects.delete(each=True)


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


def _setup_database():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    return engine, database


class PotatoModel(ormar.Model):
    class Meta(BaseMeta):
        pass

    id = ormar.Integer(primary_key=True)
    thickness = ormar.Float()
    mass = ormar.Float()
    color = ormar.String(max_length=255)
    type = ormar.String(max_length=255)


class CarrotModel(ormar.Model):
    class Meta(BaseMeta):
        pass

    id = ormar.Integer(primary_key=True)
    length = ormar.Float()
    color = ormar.String(max_length=255)


class PotatoTypeModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "potato_type"

    name = ormar.String(primary_key=True, max_length=300)
    origin = ormar.String(max_length=300)


class CustomPotatoModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "custom_potatoes"

    potato_id = ormar.Integer(primary_key=True)
    thickness = ormar.Float()
    mass = ormar.Float()
    color = ormar.String(max_length=255)
    type = ormar.String(max_length=255)


class UniquePotatoModel(ormar.Model):
    class Meta(BaseMeta):
        pass

    id = ormar.Integer(primary_key=True)
    thickness = ormar.Float()
    mass = ormar.Float()
    color = ormar.String(max_length=255, unique=True)
    type = ormar.String(max_length=255)


def get_app():
    [
        os.remove(f"./db.sqlite3{s}")
        for s in ["", "-wal", "-shm"]
        if os.path.exists(f"./db.sqlite3{s}")
    ]

    _setup_database()

    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    return app


def ormar_implementation(**kwargs):
    app = get_app()

    router_settings = [
        dict(
            schema=PotatoModel,
            prefix="potato",
            paginate=PAGINATION_SIZE,
        ),
        dict(
            schema=CarrotModel,
            update_schema=CarrotUpdate,
            prefix="carrot",
            tags=CUSTOM_TAGS,
        ),
    ]

    return (
        app,
        OrmarCRUDRouter,
        router_settings,
    )


# noinspection DuplicatedCode
def ormar_implementation_custom_ids():
    app = get_app()

    app.include_router(
        OrmarCRUDRouter(
            schema=CustomPotatoModel,
            prefix="potatoes",
            paginate=PAGINATION_SIZE,
        )
    )

    return app


def ormar_implementation_string_pk():
    app = get_app()

    app.include_router(
        OrmarCRUDRouter(
            schema=PotatoTypeModel,
            prefix="potato_type",
        )
    )

    return app


def ormar_implementation_integrity_errors():
    app = get_app()

    app.include_router(
        OrmarCRUDRouter(
            schema=UniquePotatoModel,
            prefix="potatoes",
            paginate=PAGINATION_SIZE,
        )
    )
    app.include_router(
        OrmarCRUDRouter(
            schema=CarrotModel,
            create_schema=CarrotCreate,
            update_schema=CarrotUpdate,
            prefix="carrots",
        )
    )

    return app
