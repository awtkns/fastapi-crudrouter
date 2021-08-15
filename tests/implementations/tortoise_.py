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
)


class PotatoModel(Model):
    thickness = fields.FloatField()
    mass = fields.FloatField()
    color = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)


class CarrotModel(Model):
    length = fields.FloatField()
    color = fields.CharField(max_length=255)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["tests.implementations.tortoise_"],
            "default_connection": "default",
        },
    },
}


async def on_shutdown():
    await Tortoise.close_connections()


def tortoise_implementation(**kwargs):
    [
        os.remove(f"./db.sqlite3{s}")
        for s in ["", "-wal", "-shm"]
        if os.path.exists(f"./db.sqlite3{s}")
    ]

    app = FastAPI(on_shutdown=[on_shutdown])

    Tortoise.init(config=TORTOISE_ORM)
    Tortoise.generate_schemas()

    router_settings = [
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

    return app, TortoiseCRUDRouter, router_settings
