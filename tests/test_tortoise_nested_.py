from types import SimpleNamespace

from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.exceptions import IntegrityError
from tests.conftest import yield_test_client
from typing import List

import pytest
from fastapi_crudrouter.core.tortoise import TortoiseCRUDRouter
from pydantic import BaseModel
from tortoise import Tortoise, Model, fields

from tests import ORMModel, test_router
from tests.implementations.tortoise_ import _setup_base_app, Parent, Child
from tests.implementations import tortoise_
from pydantic import ValidationError

CHILD_URL = "/child"
PARENT_URL = "/parent"


TORTOISE_ORM = {
    "connections": {"default": "sqlite://:memory:"},
    "apps": {
        "models": {
            "models": ["tests.test_tortoise_nested_"],
        },
    },
}


# Schemas created in the module body, before Tortoise has initiated
ChildNoInitSchema = pydantic_model_creator(Child, name="ChildNoInitSchema")
ChildNoInitCreate = pydantic_model_creator(
    Child, name="ChildNoInitCreate", exclude_readonly=True
)
ParentNoInitSchema = pydantic_model_creator(
    Parent, name="ParentNoInitSchema", exclude=("age",)
)
ParentNoInitCreate = pydantic_model_creator(
    Parent, name="ParentNoInitCreate", exclude_readonly=True, exclude=("age",)
)


def base_schemas():
    class ChildSchema(ORMModel):
        parent_id: int

    class ChildCreate(BaseModel):
        parent_id: int

    class ParentSchema(ORMModel):
        children: List[ChildSchema] = []

    class ParentCreate(BaseModel):
        pass

    print(ParentCreate.schema_json(indent=2))

    return ChildSchema, ChildCreate, ParentSchema, ParentCreate


def tortoise_init_schemas():
    Tortoise.init_models([tortoise_], "models")
    ChildSchema = pydantic_model_creator(
        Child, name="ChildSchemaInit", exclude=("parent", "parent_id")
    )
    ChildCreate = pydantic_model_creator(
        Child, name="ChildCreateInit", exclude_readonly=True
    )
    ParentSchema = pydantic_model_creator(
        Parent, name="ParentSchemaInit", exclude=("age",)
    )
    ParentCreate = pydantic_model_creator(
        Parent, name="ParentCreateInit", exclude_readonly=True, exclude=("age",)
    )

    return ChildSchema, ChildCreate, ParentSchema, ParentCreate


def tortoise_no_init_schemas():
    return ChildNoInitSchema, ChildNoInitCreate, ParentNoInitSchema, ParentNoInitCreate


async def on_startup():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def on_shutdown():
    await Tortoise.close_connections()


@pytest.fixture
def tortoise_client():
    ns = SimpleNamespace()
    ns.__name__ = "tests.implementations.tortoise_"
    app = _setup_base_app()
    for c in yield_test_client(app, ns):
        yield app, c


def test_nested_models_pydantic_schemas(tortoise_client):
    """
    Tortoise will not fetch the related fields (Parent -> Child) automatically,
    therefore the data for the children will be missing.
    """
    app, client = tortoise_client
    ChildSchema, ChildCreate, ParentSchema, ParentCreate = base_schemas()

    app.include_router(
        TortoiseCRUDRouter(
            schema=ParentSchema,
            create_schema=ParentCreate,
            db_model=Parent,
            prefix=PARENT_URL,
        )
    )
    app.include_router(
        TortoiseCRUDRouter(
            schema=ChildSchema,
            create_schema=ChildCreate,
            db_model=Child,
            prefix=CHILD_URL,
        )
    )

    with pytest.raises(ValidationError):
        test_router.test_post(client, PARENT_URL, dict())


def test_nested_models_tortoise_no_init(tortoise_client):
    """
    Pydantic models created with pydantic_model_creator, with models that where not
    initiated will not have the relations mapped, therefore the parent_id field in
    the Child, neither the Parent will have a children field in its model
    """
    app, client = tortoise_client
    ChildSchema, ChildCreate, ParentSchema, ParentCreate = tortoise_no_init_schemas()

    app.include_router(
        TortoiseCRUDRouter(
            schema=ParentSchema,
            create_schema=ParentCreate,
            db_model=Parent,
            prefix=PARENT_URL,
        )
    )
    app.include_router(
        TortoiseCRUDRouter(
            schema=ChildSchema,
            create_schema=ChildCreate,
            db_model=Child,
            prefix=CHILD_URL,
        )
    )

    parent = test_router.test_post(client, PARENT_URL, dict())
    with pytest.raises(IntegrityError):
        test_router.test_post(client, CHILD_URL, dict(parent_id=parent["id"]))

    res = client.get(f'{PARENT_URL}/{parent["id"]}')
    assert res.status_code == 200, res.json()
    parent_data = res.json()

    with pytest.raises(KeyError):
        type(parent_data["children"])


def test_nested_models_tortoise(tortoise_client):
    """
    Pydantic models created with pydantic_model_creator where the models already
    have been initiated should return the models populated with its related objects
    """
    app, client = tortoise_client
    ChildSchema, ChildCreate, ParentSchema, ParentCreate = tortoise_init_schemas()

    app.include_router(
        TortoiseCRUDRouter(
            schema=ParentSchema,
            create_schema=ParentCreate,
            db_model=Parent,
            prefix=PARENT_URL,
        )
    )
    app.include_router(
        TortoiseCRUDRouter(
            schema=ChildSchema,
            create_schema=ChildCreate,
            db_model=Child,
            prefix=CHILD_URL,
        )
    )

    parent = test_router.test_post(client, PARENT_URL, dict())
    child = test_router.test_post(client, CHILD_URL, dict(parent_id=parent["id"]))

    res = client.get(f'{PARENT_URL}/{parent["id"]}')
    assert res.status_code == 200, res.json()
    parent_data = res.json()

    res = client.get(f'{CHILD_URL}/{child["id"]}')
    assert res.status_code == 200, res.json()
    child_data = res.json()

    assert type(parent_data["children"]) is list, parent_data
    assert parent_data["children"][0] == child_data
