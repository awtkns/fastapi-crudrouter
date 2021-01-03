from typing import Callable
from pydantic import BaseModel


from . import CRUDGenerator, NOT_FOUND


class MemoryCRUDRouter(CRUDGenerator):
    
    def __init__(self, schema: BaseModel, *args, **kwargs):
        super(MemoryCRUDRouter, self).__init__(schema, *args, **kwargs)
        self.models = []
        self._id = 0

    def _get_all(self) -> Callable:
        def route():
            return self.models
        return route

    def _get_one(self) -> Callable:
        def route(item_id: int):
            for m in self.models:
                if m.id == item_id:
                    return m

            raise NOT_FOUND

        return route

    def _create(self) -> Callable:
        def route(model: self.schema):
            model.id = self._get_next_id()
            self.models.append(model)
            return model

        return route

    def _update(self) -> Callable:
        def route(item_id: int, model: self.schema):
            for i, m in enumerate(self.models):
                if m.id == item_id:
                    model.id = m.id
                    self.models[i] = model
                    return model

            raise NOT_FOUND
        return route

    def _delete_all(self) -> Callable:
        def route():
            self.models = []
            return self.models

        return route

    def _delete_one(self) -> Callable:
        def route(item_id: int):
            for i, m in enumerate(self.models):
                if m.id == item_id:
                    del self.models[i]
                    return m

            raise NOT_FOUND

        return route

    def _get_next_id(self) -> int:
        id = self._id
        self._id += 1

        return id
