import os

from fastapi import FastAPI
from tortoise import Model, Tortoise, fields


from fastapi_crudrouter import TortoiseCRUDRouter

from tests import (
    Carrot,
    CarrotCreate,
    CarrotUpdate,
    PAGINATION_SIZE,
    Potato,
    CUSTOM_TAGS,
    config,
)
from tests.implementations import BaseImpl
from tests.implementations._base import SETTINGS


class PotatoModel(Model):
    thickness = fields.FloatField()
    mass = fields.FloatField()
    color = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)


class CarrotModel(Model):
    length = fields.FloatField()
    color = fields.CharField(max_length=255)


class TortoiseImpl(BaseImpl):
    __router__ = TortoiseCRUDRouter
    __backends__ = ["aiosqlite://db.sqlite3"]

    def get_app(self) -> FastAPI:
        app = super().get_app()
        tortoise_config = {
            "connections": {"default": self.uri},
            "apps": {
                "models": {
                    "models": ["tests.implementations.tortoise_"],
                    "default_connection": "default",
                },
            },
        }

        @app.on_event("startup")
        async def startup():
            await Tortoise.init(config=tortoise_config)
            await Tortoise.generate_schemas()

        @app.on_event("shutdown")
        async def shutdown():
            await Tortoise.close_connections()

        return app

    def default_impl(self) -> SETTINGS:
        return [
            dict(
                schema=Potato,
                db_model=PotatoModel,
                prefix="potato",
                paginate=PAGINATION_SIZE,
            ),
            dict(
                schema=Carrot,
                db_model=CarrotModel,
                create_schema=CarrotCreate,
                update_schema=CarrotUpdate,
                prefix="carrot",
                tags=CUSTOM_TAGS,
            ),
        ]

    def integrity_errors_impl(self) -> SETTINGS:
        pass
