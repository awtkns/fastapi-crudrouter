from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TYPE_CHECKING,
    Type,
    TypeVar,
    cast,
)

from . import CRUDGenerator, NOT_FOUND, T, _utils

try:
    import ormar
    from ormar import Model
except ImportError:
    ormar_installed = False
else:
    ormar_installed = True
OR = TypeVar("OR", bound="Model")


class OrmarCRUDRouter(CRUDGenerator[OR]):
    if TYPE_CHECKING:
        schema: Type[OR]

    def __init__(self, schema: Type[OR], *args: Any, **kwargs: Any) -> None:
        assert ormar_installed, "Ormar must be installed to use the OrmarCRUDRouter."

        self._pk: str = schema.Meta.pkname
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        if "prefix" not in kwargs:
            kwargs["prefix"] = schema.Meta.tablename
        if "create_schema" not in kwargs:
            kwargs["create_schema"] = schema
        if "update_schema" not in kwargs:
            kwargs["update_schema"] = schema

        super().__init__(schema, *args, **kwargs)

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable:
        async def route(
            pagination: Dict = self.pagination,  # type: ignore
        ) -> List[Optional[OR]]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            query = self.schema.objects.offset(cast(int, skip))
            if limit:
                query = query.limit(cast(int, limit))
            return await query.all()

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable:
        async def route(item_id: self._pk_type) -> OR:  # type: ignore
            try:
                filter_ = {self._pk: item_id}
                model = await self.schema.objects.filter(
                    _exclude=False, **filter_
                ).first()
            except ormar.NoMatch:
                raise NOT_FOUND
            return model

        return route

    def _create(self, *args: Any, **kwargs: Any) -> Callable:
        async def route(model: self.create_schema) -> OR:  # type: ignore
            model_dict = model.dict()
            if self.schema.Meta.model_fields[self._pk].autoincrement:
                model_dict.pop(self._pk, None)
            return await self.schema.objects.create(**model.dict())

        return route

    def _update(self, *args: Any, **kwargs: Any) -> Callable:
        async def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
        ) -> OR:
            filter_ = {self._pk: item_id}
            await self.schema.objects.filter(_exclude=False, **filter_).update(
                **model.dict(exclude_unset=True)
            )
            return await self._get_one()(item_id)

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable:
        async def route() -> List[Optional[OR]]:
            await self.schema.objects.delete(each=True)
            return await self._get_all()(pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable:
        async def route(item_id: self._pk_type) -> OR:  # type: ignore
            model = await self._get_one()(item_id)
            await model.delete()
            return model

        return route
