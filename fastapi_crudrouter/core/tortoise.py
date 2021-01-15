import asyncio
from typing import Callable
from fastapi import Depends
from pydantic import BaseModel

from . import CRUDGenerator, NOT_FOUND

try:
    # from sqlalchemy.orm import Session
    from tortoise import Tortoise, run_async
    from tortoise.models import Model
    from tortoise.contrib.fastapi import register_tortoise
except ImportError:
    tortoise_installed = False
    Session = None
    DeclarativeMeta = None
else:
    tortoise_installed = True

try:
    from database.tortoise_config import TORTOISE_ORM

    # register_tortoise(app, config=TORTOISE_ORM)
    print("tortoise config found")
except ImportError:
    print("cannot find tortoise config")


class TortoiseCRUDRouter(CRUDGenerator):

    def __init__(self, schema: BaseModel, db_model: Model, config: dict, *args, **kwargs):
        assert tortoise_installed, "Tortoise ORM must be installed to use the TortoiseCRUDRouter."

        self.db_model = db_model
        self._primary_key: str = db_model.describe()['pk_field']['db_column']

        # todo add the other methods of configuration (got config, need file and link+modules)
        # Tortoise.init(config=config)

        if 'prefix' not in kwargs:
            # unsure why the name has a "None." appended but I handle it
            kwargs['prefix'] = db_model.describe()['name'].replace('None.', '')

        if 'create_schema' not in kwargs:
            kwargs['create_schema'] = self.schema_factory(schema, self._primary_key)

        super().__init__(schema, *args, **kwargs)

    def _get_all(self) -> Callable:
        async def route():
            models = await self.db_model.all()
            return models

        return route

    def _get_one(self) -> Callable:
        async def route(item_id):
            # todo this aint it chief
            model = await self.db_model.filter(id=item_id).first()

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(self) -> Callable:
        async def route(model: self.create_schema):
            db_model = self.db_model(**model.dict())
            await db_model.save()

            return db_model

        return route

    def _update(self) -> Callable:
        def route(item_id: int, model: self.schema):
            raise NotImplementedError

        return route

    def _delete_all(self) -> Callable:
        def route():
            raise NotImplementedError

        return route

    def _delete_one(self) -> Callable:
        def route(item_id: int):
            raise NotImplementedError

        return route
