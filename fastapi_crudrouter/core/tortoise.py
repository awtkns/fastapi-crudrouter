from typing import Callable
from pydantic import BaseModel

from . import CRUDGenerator, NOT_FOUND

try:
    from tortoise import Tortoise
    from tortoise.models import Model
except ImportError:
    tortoise_installed = False
else:
    tortoise_installed = True


class TortoiseCRUDRouter(CRUDGenerator):

    def __init__(self, schema: BaseModel, db_model, *args, **kwargs):
        assert tortoise_installed, "Tortoise ORM must be installed to use the TortoiseCRUDRouter."

        self.db_model = db_model
        self._primary_key: str = db_model.describe()['pk_field']['db_column']

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
        async def route(item_id: int, model: self.create_schema):
            await self.db_model.filter(id=item_id).update(**model.dict(exclude_unset=True))
            return await self._get_one()(item_id)

        return route

    def _delete_all(self) -> Callable:
        async def route():
            await self.db_model.all().delete()
            return await self._get_all()()

        return route

    def _delete_one(self) -> Callable:
        async def route(item_id: int):
            model = await self._get_one()(item_id)
            await self.db_model.filter(id=item_id).delete()

            return model

        return route
