from typing import Callable

from . import CRUDGenerator, NOT_FOUND


class MemoryCRUDRouter(CRUDGenerator):
    models = []

    def get_all(self) -> Callable:
        def route():
            return self.models
        return route

    def get_one(self) -> Callable:
        def route(item_id: int):
            for m in models:
                if m.id == item_id:
                    return m

            raise NOT_FOUND

        return route

    def create(self) -> Callable:
        def route(model: self.model_cls):
            self.models.append(model)
            return model

        return route

    def update(self) -> Callable:
        def route(item_id: int, model: self.model_cls):
            for i, m in enumerate(self.models):
                if m.id == item_id:
                    self.models[i] = model
                    return model
            raise NOT_FOUND
        return route

    def delete_all(self) -> Callable:
        def route():
            self.models = []
            return self.models

        return route

    def delete_one(self) -> Callable:
        def route(item_id: int):
            for i, m in enumerate(self.models):
                if m.id == item_id:
                    self.models.remove(i)
                    return m

            raise NOT_FOUND

        return route
