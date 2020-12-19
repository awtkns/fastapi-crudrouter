from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

models = []

NOT_FOUND = HTTPException(404, 'Item not found')


class CRUDGenerator(APIRouter):
    model_cls: BaseModel = None
    _base_path: str = '/'

    def __init__(self, model: BaseModel, *args, **kwargs):
        self.model_cls = model
        self._base_path += self.model_cls.__name__.lower()

        super().__init__(prefix=self._base_path, tags=[self._base_path.strip('/')], *args, **kwargs)

        def get_all():
            return models

        def get_one(item_id):
            for m in models:
                if m.id == item_id:
                    return m
            raise NOT_FOUND

        def create(model: model):
            models.append(model)

            return model

        def update(item_id: int, model: model):
            for i, m in enumerate(models):
                if m.id == item_id:
                    models[i] = model
                    return model
            raise NOT_FOUND

        def delete_all():
            models = []
            return models

        def delete_one(item_id):
            for i, m in enumerate(models):
                if m.id == item_id:
                    models.remove(i)
                    return m

            raise NOT_FOUND

        super().add_api_route('', get_all, methods=['GET'], response_model=List[self.model_cls])
        super().add_api_route('', create, methods=['POST'], response_model=self.model_cls)
        super().add_api_route('', delete_all, methods=['DELETE'], response_model=List[self.model_cls])

        super().add_api_route('/{item_id}', get_one, methods=['GET'], response_model=self.model_cls)
        super().add_api_route('/{item_id}', update, methods=['POST'], response_model=self.model_cls)
        super().add_api_route('/{item_id}', delete_one, methods=['DELETE'], response_model=self.model_cls)

