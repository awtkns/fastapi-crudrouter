from typing import Any, Callable, List, Type, TypeVar, cast, Coroutine

from . import CRUDGenerator, NOT_FOUND, T, _utils

try:
    from tortoise.models import Model
except ImportError:
    tortoise_installed = False
else:
    tortoise_installed = True
TM = TypeVar("TM", bound="Model")


class TortoiseCRUDRouter(CRUDGenerator[T]):
    def __init__(
        self, schema: Type[T], db_model: Type[TM], *args: Any, **kwargs: Any
    ) -> None:
        assert (
            tortoise_installed
        ), "Tortoise ORM must be installed to use the TortoiseCRUDRouter."

        self.db_model = db_model
        self._pk: str = db_model.describe()["pk_field"]["db_column"]

        if "prefix" not in kwargs:
            # unsure why the name has a "None." appended but I handle it
            kwargs["prefix"] = db_model.describe()["name"].replace("None.", "")

        if "create_schema" not in kwargs:
            kwargs["create_schema"] = _utils.schema_factory(schema, self._pk)

        super().__init__(schema, *args, **kwargs)

    def _get_all(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, List[TM]]]:
        async def route(pagination: dict = self.pagination) -> List[TM]:  # type: ignore
            skip, limit = pagination.get("skip"), pagination.get("limit")
            query = self.db_model.all().offset(cast(int, skip))
            if limit:
                query = query.limit(cast(int, limit))
            return await query

        return route

    def _get_one(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, TM]]:
        async def route(item_id: int) -> TM:
            model = await self.db_model.filter(id=item_id).first()

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, TM]]:
        async def route(model: self.create_schema) -> TM:  # type: ignore
            db_model = self.db_model(**model.dict())
            await db_model.save()

            return db_model

        return route

    def _update(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, TM]]:
        async def route(item_id: int, model: self.update_schema) -> TM:  # type: ignore
            await self.db_model.filter(id=item_id).update(
                **model.dict(exclude_unset=True)
            )
            return await self._get_one()(item_id)

        return route

    def _delete_all(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, List[TM]]]:
        async def route() -> List[TM]:
            await self.db_model.all().delete()
            return await self._get_all()(pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, TM]]:
        async def route(item_id: int) -> TM:
            model: TM = await self._get_one()(item_id)
            await self.db_model.filter(id=item_id).delete()

            return model

        return route
