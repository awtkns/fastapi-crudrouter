from typing import Any, Callable, List, Type

from . import CRUDGenerator, NOT_FOUND, T


class MemoryCRUDRouter(CRUDGenerator[T]):
    def __init__(self, schema: Type[T], *args: Any, **kwargs: Any) -> None:
        super(MemoryCRUDRouter, self).__init__(schema, *args, **kwargs)
        self.models: List[T] = []
        self._id = 1

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[T]]:
        def route(pagination: dict = self.pagination) -> List[T]:  # type: ignore
            skip, limit = pagination.get("skip"), pagination.get("limit")

            if limit:
                return self.models[skip : skip + limit]
            else:
                return self.models[skip:]

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., T]:
        def route(item_id: int) -> T:
            for model in self.models:
                if model.id == item_id:  # type: ignore
                    return model

            raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., T]:
        def route(model: self.create_schema) -> T:  # type: ignore
            model_dict = model.dict()
            model_dict["id"] = self._get_next_id()
            ready_model = self.schema(**model_dict)
            self.models.append(ready_model)
            return ready_model

        return route

    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., T]:
        def route(item_id: int, model: self.update_schema) -> T:  # type: ignore
            for ind, model_ in enumerate(self.models):
                if model_.id == item_id:  # type: ignore
                    self.models[ind] = self.schema(
                        **model.dict(), id=model_.id  # type: ignore
                    )
                    return self.models[ind]

            raise NOT_FOUND

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[T]]:
        def route() -> List[T]:
            self.models = []
            return self.models

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., T]:
        def route(item_id: int) -> T:
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
