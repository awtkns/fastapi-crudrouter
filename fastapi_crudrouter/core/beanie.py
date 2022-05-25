from typing import Any, Callable, Dict, List, Type, cast, Coroutine, Optional, Union

from fastapi import HTTPException

from . import CRUDGenerator, NOT_FOUND, _utils
from ._types import DEPENDENCIES, PAGINATION

try:
    from beanie import Document
    from beanie.odm.fields import PydanticObjectId
except ImportError:
    Document = None  # type: ignore
    beanie_installed = False
else:
    beanie_installed = True


CALLABLE = Callable[..., Coroutine[Any, Any, Document]]
CALLABLE_LIST = Callable[..., Coroutine[Any, Any, List[Optional[Document]]]]


class BeanieCRUDRouter(CRUDGenerator[Document]):
    def __init__(
        self,
        schema: Type[Document],
        create_schema: Optional[Type[Document]] = None,
        update_schema: Optional[Type[Document]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = True,
        **kwargs: Any
    ) -> None:
        assert (
            beanie_installed
        ), "Beanie ODM must be installed to use the BeanieCRUDRouter."

        # TODO: Beanie only supports `id` as the primary field, when other
        # fields get supported, this part needs to be updated
        self._pk: str = 'id'
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        super().__init__(
            schema=schema,
            create_schema=create_schema or schema,
            update_schema=update_schema or schema,
            prefix=prefix or schema.Settings.name,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs
        )

        self._INTEGRITY_ERROR = self._get_integrity_error_type()

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
            pagination: PAGINATION = self.pagination,
        ) -> List[Optional[Document]]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            query = await self.schema.all(
                skip=cast(int, skip),
                limit=limit
            ).to_list()
            return query  # type: ignore

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: self._pk_type) -> Document:  # type: ignore
            model = await self.schema.get(
                item_id
            )
            if model is None:
                raise NOT_FOUND from None
            return model

        return route

    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(model: self.create_schema) -> Document:  # type: ignore
            model_dict = model.dict()
            if self._pk_type == PydanticObjectId:
                model_dict.pop(self._pk, None)
            try:
                document: Type[Document] = self.schema(**model_dict)
                return await self.schema.insert_one(document)  # TODO: Test
            except self._INTEGRITY_ERROR:
                raise HTTPException(422, "Key already exists") from None

        return route

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
        ) -> Document:
            try:
                update_query: Dict = {
                    "$set": {
                        field: value
                        for field, value in model.dict(exclude_unset=True).items()
                    }
                }
                await self.schema.get(item_id).update( update_query)  # TODO: Test
            except self._INTEGRITY_ERROR as e:
                self._raise(e)
            return await self._get_one()(item_id)

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route() -> List[Optional[Document]]:
            await self.schema.delete_all()
            return await self._get_all()(pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(item_id: self._pk_type) -> Document:  # type: ignore
            model = await self._get_one()(item_id)
            await model.delete()
            return model

        return route

    def _get_integrity_error_type(self) -> Type[Exception]:
        """Imports the Integrity exception based on the used backend"""
        # TODO: All Beanie exceptions are children of Exception class, so
        # plain `Exception` should work. Although a more definite exception
        # might be needed.
        return Exception
