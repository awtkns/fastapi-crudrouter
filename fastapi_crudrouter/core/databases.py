from typing import Any, Callable, List, Mapping, Type, Coroutine

from fastapi import HTTPException

from . import CRUDGenerator, NOT_FOUND, T, _utils

try:
    from sqlalchemy.sql.schema import Table
    from databases.core import Database
except ImportError:
    databases_installed = False
else:
    databases_installed = True


class DatabasesCRUDRouter(CRUDGenerator[T]):
    def __init__(
        self,
        schema: Type[T],
        table: "Table",
        database: "Database",
        *args: Any,
        **kwargs: Any
    ) -> None:
        assert (
            databases_installed
        ), "Databases and SQLAlchemy must be installed to use the DatabasesCRUDRouter."
        self.table = table
        self.db = database
        self._pk = table.primary_key.columns.values()[0].name
        self._pk_col = self.table.c[self._pk]
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        if "prefix" not in kwargs:
            kwargs["prefix"] = table.name

        if "create_schema" not in kwargs:
            kwargs["create_schema"] = _utils.schema_factory(schema, self._pk)

        super().__init__(schema, *args, **kwargs)

    def _get_all(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, List[Mapping[Any, Any]]]]:
        async def route(
            pagination: dict = self.pagination,  # type: ignore
        ) -> List[Mapping[Any, Any]]:
            skip, limit = pagination.get("skip"), pagination.get("limit")

            query = self.table.select().limit(limit).offset(skip)
            return await self.db.fetch_all(query)

        return route

    def _get_one(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, Mapping[Any, Any]]]:
        async def route(item_id: self._pk_type) -> Mapping:  # type: ignore
            query = self.table.select().where(self._pk_col == item_id)
            model = await self.db.fetch_one(query)

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, Mapping[Any, Any]]]:
        async def route(
            schema: self.create_schema,  # type: ignore
        ) -> Mapping[Any, Any]:
            try:
                query = self.table.insert()
                rid = await self.db.execute(query=query, values=schema.dict())
                return {self._pk: rid, **schema.dict()}
            except Exception:
                raise HTTPException(422, "Key already exists")

        return route

    def _update(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, Mapping[Any, Any]]]:
        async def route(
            item_id: self._pk_type, schema: self.update_schema  # type: ignore
        ) -> Mapping[Any, Any]:
            query = self.table.update().where(self._pk_col == item_id)
            rid = await self.db.execute(
                query=query, values=schema.dict(exclude={self._pk})
            )

            if rid:
                return {self._pk: rid, **schema.dict()}
            else:
                raise NOT_FOUND

        return route

    def _delete_all(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, List[Mapping[Any, Any]]]]:
        async def route() -> List[Mapping[Any, Any]]:
            query = self.table.delete()
            await self.db.execute(query=query)

            return await self._get_all()(pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(
        self, *args: Any, **kwargs: Any
    ) -> Callable[..., Coroutine[Any, Any, Mapping[Any, Any]]]:
        async def route(item_id: self._pk_type) -> Mapping[Any, Any]:  # type: ignore
            query = self.table.delete().where(self._pk_col == item_id)

            row = await self._get_one()(item_id)
            rid = await self.db.execute(query=query)

            if rid:
                return row
            else:
                raise NOT_FOUND

        return route
