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

from tests.implementations import BaseImpl
from tests.implementations._base import SETTINGS


class GinoImpl(BaseImpl):
    __router__ = GinoCRUDRouter
    __backends__ = [config.POSTGRES_URI]

    def __init__(self, *args, **kwargs):
        super(GinoImpl, self).__init__(*args, **kwargs)
        self.uri = self.uri.replace("postgresql", "asyncpg")
        self.db = None

    async def _migrate(self):
        async with self.db.with_bind(self.uri):
            await self.db.gino.create_all()

    def get_app(self) -> FastAPI:
        app = super().get_app()
        self.db.init_app(app)

        return app

    def default_impl(self) -> SETTINGS:
        db = Gino(dsn=self.uri)

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

        self.db = db
        asyncio.get_event_loop().run_until_complete(self._migrate())

        return [
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

    def integrity_errors_impl(self) -> SETTINGS:
        pass
