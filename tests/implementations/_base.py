from abc import ABC, abstractmethod
from typing import Type, Dict, Any, List

SETTINGS = List[Dict[str, Any]]

from fastapi import FastAPI
from fastapi_crudrouter.core import CRUDGenerator

from tests.conf import Datasource


class BaseImpl(ABC):
    def __init__(self, datasource):
        self.datasource = datasource
        self.uri = datasource.uri

    def __repr__(self):
        return f"{self.__class__.__name__}-{self.datasource.name}"

    @staticmethod
    def single_router(func):
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs)]

        return wrapper

    def get_app(self) -> FastAPI:
        return FastAPI(title=self.__class__.__name__, description=f"Backend={self.uri}")

    @staticmethod
    @abstractmethod
    def get_router() -> Type[CRUDGenerator]:
        pass

    @staticmethod
    @abstractmethod
    def supported_backends() -> List[str]:
        pass

    @abstractmethod
    def default_impl(self) -> SETTINGS:
        pass

    @abstractmethod
    def integrity_errors_impl(self) -> SETTINGS:
        pass


def create_implementation(impl: BaseImpl) -> FastAPI:
    app = impl.get_app()
    router = impl.get_router()

    [app.include_router(router(**settings)) for settings in impl.default_impl()]

    return app
