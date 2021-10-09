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
from tests.implementations import BaseImpl
from tests.implementations._base import SETTINGS


class DatabasesImpl(BaseImpl):
    __router__ = DatabasesCRUDRouter
    __backends__ = [config.SQLITE_URI, config.POSTGRES_URI]

    def __init__(self, *args, **kwargs):
        super(DatabasesImpl, self).__init__(*args, **kwargs)
        self.db = None

    def get_app(self) -> FastAPI:
        app = super().get_app()

        @app.on_event("startup")
        async def startup():
            await self.db.connect()

        @app.on_event("shutdown")
        async def shutdown():
            await self.db.disconnect()

        return app

    def default_impl(self) -> SETTINGS:
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

        self.db = databases.Database(self.uri)
        engine = create_engine(self.uri)
        metadata.create_all(bind=engine)

        return [
            dict(
                database=self.db,
                table=potatoes,
                schema=Potato,
                prefix="potato",
                paginate=PAGINATION_SIZE,
            ),
            dict(
                database=self.db,
                table=carrots,
                schema=Carrot,
                create_schema=CarrotCreate,
                update_schema=CarrotUpdate,
                prefix="carrot",
                tags=CUSTOM_TAGS,
            ),
        ]

    def integrity_errors_impl(self) -> SETTINGS:
        pass
