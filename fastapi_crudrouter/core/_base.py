from typing import List, Optional, Callable

from starlette.routing import Route
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, create_model

models = []

NOT_FOUND = HTTPException(404, 'Item not found')


class CRUDGenerator(APIRouter):
    schema: BaseModel = None
    _base_path: str = '/'

    def __init__(
        self,
        schema: BaseModel,
        create_schema: BaseModel = None,
        prefix: str = None,
        get_all_route: bool = True,
        get_one_route: bool = True,
        create_route: bool = True,
        update_route: bool = True,
        delete_one_route: bool = True,
        delete_all_route: bool = True,
        *args,
        **kwargs
    ):

        self.schema = schema
        self.create_schema = create_schema if create_schema else self.schema_factory(self.schema)

        prefix = self._base_path + (self.schema.__name__.lower() if not prefix else prefix).strip('/')
        super().__init__(prefix=prefix, tags=[prefix.strip('/').capitalize()], *args, **kwargs)

        if get_all_route:
            super().add_api_route('', self._get_all(), methods=['GET'], response_model=Optional[List[self.schema]], summary='Get All')

        if create_route:
            super().add_api_route('', self._create(), methods=['POST'], response_model=self.schema, summary='Create One')

        if delete_all_route:
            super().add_api_route('', self._delete_all(), methods=['DELETE'], response_model=Optional[List[self.schema]], summary='Delete All')

        if get_one_route:
            super().add_api_route('/{item_id}', self._get_one(), methods=['GET'], response_model=self.schema, summary='Get One')

        if update_route:
            super().add_api_route('/{item_id}', self._update(), methods=['PUT'], response_model=self.schema, summary='Update One')

        if delete_one_route:
            super().add_api_route('/{item_id}', self._delete_one(), methods=['DELETE'], response_model=self.schema, summary='Delete One')

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
            if r.path == f'{self.prefix}{path}' and r.methods == methods:
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

    @staticmethod
    def schema_factory(schema_cls: BaseModel, pk_field_name: str = 'id'):
        """
        Is used to create a CreateSchema which does not contain pk
        """

        fields = {f.name: (f.type_, ...) for f in schema_cls.__fields__.values() if f.name != pk_field_name}

        name = schema_cls.__name__ + 'Create'
        schema = create_model(name, **fields)
        return schema
