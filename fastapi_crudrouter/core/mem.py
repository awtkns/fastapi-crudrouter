from typing import Any, Callable, List, Type, cast
from pydantic import BaseModel

from . import CRUDGenerator, NOT_FOUND
from ._types import PAGINATION, PYDANTIC_SCHEMA as SCHEMA


class MemoryCRUDRouter(CRUDGenerator[SCHEMA]):
    def __init__(self, schema: Type[SCHEMA], *args: Any, **kwargs: Any) -> None:
        super(MemoryCRUDRouter, self).__init__(schema, *args, **kwargs)
        self.models: List[BaseModel] = []
        self._id = 1

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[SCHEMA]]:
        def route(pagination: PAGINATION = self.pagination) -> List[SCHEMA]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            skip = cast(int, skip)

            return (
                self.models[skip:]
                if limit is None
                else self.models[skip : skip + limit]
            )

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., SCHEMA]:
        def route(item_id: int) -> SCHEMA:
            for model in self.models:
                if model.id == item_id:  # type: ignore
                    return model

            raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., SCHEMA]:
        def route(model: self.create_schema) -> SCHEMA:  # type: ignore
            model_dict = model.dict()
            model_dict["id"] = self._get_next_id()
            ready_model = self.schema(**model_dict)
            self.models.append(ready_model)
            return ready_model

        return route

    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., SCHEMA]:
        def route(item_id: int, model: self.update_schema) -> SCHEMA:  # type: ignore
            for ind, model_ in enumerate(self.models):
                if model_.id == item_id:  # type: ignore
                    self.models[ind] = self.schema(
                        **model.dict(), id=model_.id  # type: ignore
                    )
                    return self.models[ind]

            raise NOT_FOUND

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[SCHEMA]]:
        def route() -> List[SCHEMA]:
            self.models = []
            return self.models

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., SCHEMA]:
        def route(item_id: int) -> SCHEMA:
            for ind, model in enumerate(self.models):
                if model.id == item_id:  # type: ignore
                    del self.models[ind]
                    return model

            raise NOT_FOUND

        return route

    def _get_next_id(self) -> int:
        id_ = self._id
        self._id += 1

        return id_
