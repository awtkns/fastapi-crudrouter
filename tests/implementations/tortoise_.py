import os
from typing import Awaitable

from fastapi import FastAPI
from pydantic.main import Extra
from tortoise import Model, Tortoise, fields, run_async
from tortoise.contrib.pydantic.creator import pydantic_model_creator

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


class Parent(Model):
    id = fields.IntField(pk=True)
    age = fields.IntField(null=True)
    children: fields.ReverseRelation["Child"]

    class PydanticMeta:
        max_recursion: int = 1


class Child(Model):
    id = fields.IntField(pk=True)
    parent: Awaitable[Parent] = fields.ForeignKeyField(
        "models.Parent", related_name="children", on_delete="RESTRICT"
    )  # type: ignore

    class PydanticMeta:
        max_recursion: int = 1


TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    #  "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": ["tests.implementations.tortoise_"],
            "default_connection": "default",
        },
    },
}


async def on_startup():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def on_shutdown():
    await Tortoise.close_connections()


def _setup_base_app():
    [
        os.remove(f"./db.sqlite3{s}")
        for s in ["", "-wal", "-shm"]
        if os.path.exists(f"./db.sqlite3{s}")
    ]

    return FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])


def tortoise_implementation():
    app = _setup_base_app()

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


def tortoise_implementation_no_init():
    app = _setup_base_app()

    PotatoTortoise = pydantic_model_creator(PotatoModel)
    CarrotTortoise = pydantic_model_creator(CarrotModel)
    CarrotCreateTortoise = pydantic_model_creator(
        CarrotModel, name="CarrotCreate", exclude_readonly=True
    )
    CarrotUpdateTortoise = pydantic_model_creator(
        CarrotModel, name="CarrotUpdate", exclude_readonly=True, exclude=("color",)
    )
    # Tortoise sets CarrotUpdateTortoise.__config__.extra = Extra.forbid by default
    # change to Extra.ignore to match the behaviour of other tests
    CarrotUpdateTortoise.__config__.extra = Extra.ignore

    router_settings = [
        dict(
            schema=PotatoTortoise,
            db_model=PotatoModel,
            prefix="potato",
            paginate=PAGINATION_SIZE,
        ),
        dict(
            schema=CarrotTortoise,
            db_model=CarrotModel,
            create_schema=CarrotCreateTortoise,
            update_schema=CarrotUpdateTortoise,
            prefix="carrot",
            tags=CUSTOM_TAGS,
        ),
    ]

    return app, TortoiseCRUDRouter, router_settings


def tortoise_implementation_init():
    app = _setup_base_app()

    Tortoise.init_models(TORTOISE_ORM["apps"]["models"]["models"], "models")

    PotatoTortoise = pydantic_model_creator(PotatoModel)
    CarrotTortoise = pydantic_model_creator(CarrotModel)
    CarrotCreateTortoise = pydantic_model_creator(
        CarrotModel, name="CarrotCreate", exclude_readonly=True
    )
    CarrotUpdateTortoise = pydantic_model_creator(
        CarrotModel, name="CarrotUpdate", exclude_readonly=True, exclude=("color",)
    )
    # Tortoise sets CarrotUpdateTortoise.__config__.extra = Extra.forbid by default
    # change to Extra.ignore to match the behaviour of other tests
    CarrotUpdateTortoise.__config__.extra = Extra.ignore

    router_settings = [
        dict(
            schema=PotatoTortoise,
            db_model=PotatoModel,
            prefix="potato",
            paginate=PAGINATION_SIZE,
        ),
        dict(
            schema=CarrotTortoise,
            db_model=CarrotModel,
            create_schema=CarrotCreateTortoise,
            update_schema=CarrotUpdateTortoise,
            prefix="carrot",
            tags=CUSTOM_TAGS,
        ),
    ]

    return app, TortoiseCRUDRouter, router_settings
