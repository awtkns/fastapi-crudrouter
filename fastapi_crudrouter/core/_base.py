from typing import List, Optional, Callable

from starlette.routing import Route
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

models = []

NOT_FOUND = HTTPException(404, 'Item not found')


class CRUDGenerator(APIRouter):
    model_cls: BaseModel = None
    _base_path: str = '/'

    def __init__(self, model: BaseModel, create_schema: BaseModel = None, *args, **kwargs):
        self.model_cls = model
        self.create_schema = create_schema
        self._base_path += self.model_cls.__name__.lower()

        super().__init__(prefix=self._base_path, tags=[self._base_path.strip('/')], *args, **kwargs)

        super().add_api_route('', self._get_all(), methods=['GET'], response_model=Optional[List[self.model_cls]], summary='Get All')
        super().add_api_route('', self._create(), methods=['POST'], response_model=self.model_cls, summary='Create One')
        super().add_api_route('', self._delete_all(), methods=['DELETE'], response_model=Optional[List[self.model_cls]], summary='Delete All')

        super().add_api_route('/{item_id}', self._get_one(), methods=['GET'], response_model=self.model_cls, summary='Get One')
        super().add_api_route('/{item_id}', self._update(), methods=['PUT'], response_model=self.model_cls, summary='Update One')
        super().add_api_route('/{item_id}', self._delete_one(), methods=['DELETE'], response_model=self.model_cls, summary='Delete All')

    def api_route(self, path: str, *args, **kwargs):
        """ Overrides and exiting route if it exists"""
        methods = kwargs['methods'] if 'methods' in kwargs else ['GET']
        self.remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def get(self, path, *args, **kwargs):
        self.remove_api_route(path, ['Get'])
        return super().get(path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        self.remove_api_route(path, ['POST'])
        return super().post(path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        self.remove_api_route(path, ['PUT'])
        return super().put(path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        self.remove_api_route(path, ['DELETE'])
        return super().delete(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: List[str]):
        methods = set(methods)

        for r in self.routes:
            if r.path == f'{self._base_path}{path}' and r.methods == methods:
                self.routes.remove(r)

    def _get_all(self, *args, **kwargs) -> Callable:
        raise NotImplementedError

    def _get_one(self, *args, **kwargs) -> Callable:
        raise NotImplementedError

    def _create(self, *args, **kwargs) -> Callable:
        raise NotImplementedError

    def _update(self, *args, **kwargs) -> Callable:
        raise NotImplementedError

    def _delete_one(self, *args, **kwargs) -> Callable:
        raise NotImplementedError

    def _delete_all(self, *args, **kwargs) -> Callable:
        raise NotImplementedError

    @staticmethod
    def get_routes() -> list:
        return [
            'get_all', 'create', 'delete_all', 'get_one', 'update', 'delete_one'
        ]