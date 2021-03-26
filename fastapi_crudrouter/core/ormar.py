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
    Coroutine,
)

from fastapi import HTTPException

from . import CRUDGenerator, NOT_FOUND, _utils

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

        self._INTEGRITY_ERROR = self._get_integrity_error_type()

    def _get_all(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, List[Optional[OR]]]]:
        async def route(
            pagination: Dict = self.pagination,  # type: ignore
        ) -> List[Optional[OR]]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            query = self.schema.objects.offset(cast(int, skip))
            if limit:
                query = query.limit(cast(int, limit))
            return await query.all()

        return route

    def _get_one(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, OR]]:
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

    def _create(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, OR]]:
        async def route(model: self.create_schema) -> OR:  # type: ignore
            model_dict = model.dict()
            if self.schema.Meta.model_fields[self._pk].autoincrement:
                model_dict.pop(self._pk, None)
            try:
                return await self.schema.objects.create(**model_dict)
            except self._INTEGRITY_ERROR:
                raise HTTPException(422, "Key already exists")

        return route

    def _update(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, OR]]:
        async def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
        ) -> OR:
            filter_ = {self._pk: item_id}
            try:
                await self.schema.objects.filter(_exclude=False, **filter_).update(
                    **model.dict(exclude_unset=True)
                )
            except self._INTEGRITY_ERROR as e:
                raise HTTPException(422, ", ".join(e.args))
            return await self._get_one()(item_id)

        return route

    def _delete_all(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, List[Optional[OR]]]]:
        async def route() -> List[Optional[OR]]:
            await self.schema.objects.delete(each=True)
            return await self._get_all()(pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, OR]]:
        async def route(item_id: self._pk_type) -> OR:  # type: ignore
            model = await self._get_one()(item_id)
            await model.delete()
            return model

        return route

    def _get_integrity_error_type(self) -> Type[Exception]:
        """ Imports the Integrity exception based on the used backend """
        backend = self.schema.db_backend_name()

        try:
            if backend == "sqlite":
                from sqlite3 import IntegrityError
            elif backend == "postgresql":
                from asyncpg import (  # type: ignore
                    IntegrityConstraintViolationError as IntegrityError,
                )
            else:
                from pymysql import IntegrityError  # type: ignore
            return IntegrityError
        except ImportError:
            return Exception
