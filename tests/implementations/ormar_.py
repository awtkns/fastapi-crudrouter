import os

import databases
import ormar
import pytest
import sqlalchemy
from fastapi import FastAPI

from fastapi_crudrouter import OrmarCRUDRouter
from tests import CarrotCreate, CarrotUpdate, PAGINATION_SIZE, CUSTOM_TAGS, config
from tests.implementations import BaseImpl
from tests.implementations._base import SETTINGS

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


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


class OrmarImpl(BaseImpl):
    __router__ = OrmarCRUDRouter
    __backends__ = [config.SQLITE_URI, config.POSTGRES_URI, config.MSSQL_URI]

    def get_app(self) -> FastAPI:
        app = super().get_app()
        engine = sqlalchemy.create_engine(DATABASE_URL)
        metadata.drop_all(engine)
        metadata.create_all(engine)

        @app.on_event("startup")
        async def startup():
            await database.connect()

        @app.on_event("shutdown")
        async def shutdown():
            await database.disconnect()

        return app

    def default_impl(self) -> SETTINGS:
        return [
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

    def integrity_errors_impl(self) -> SETTINGS:
        pass
