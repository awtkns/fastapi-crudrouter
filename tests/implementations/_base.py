from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Type, Dict, Any, List

SETTINGS = List[Dict[str, Any]]

from fastapi import FastAPI, APIRouter
from fastapi_crudrouter.core import CRUDGenerator

from tests.conf import Datasource


class TestCase(Enum):
    DEFAULT = auto()
    INTEGRITY_ERRORS = auto()


class BaseImpl(ABC):
    __router__ = None
    __backends__ = []

    def __init__(self, datasource):
        self._test_case_mapping = {
            TestCase.DEFAULT: self.default_impl,
            TestCase.INTEGRITY_ERRORS: self.integrity_errors_impl,
        }

        self.datasource = datasource
        self.uri = datasource.uri

    def __repr__(self):
        return f"{self.__class__.__name__}-{self.datasource.name}"

    def get_app(self) -> FastAPI:
        return FastAPI(title=self.__class__.__name__, description=f"Backend={self.uri}")

    def get_router(self) -> Type[CRUDGenerator]:
        return self.__router__

    def get_settings(self, test_case: TestCase = TestCase.DEFAULT) -> SETTINGS:
        return self._test_case_mapping.get(test_case, self.default_impl)()

    def create_routers(self, settings: SETTINGS) -> List[APIRouter]:
        return [self.get_router()(**s) for s in settings]

    def create(
        self, test_case: TestCase = TestCase.DEFAULT, settings: SETTINGS = None
    ) -> FastAPI:
        settings = settings if settings else self.get_settings(test_case)

        app = self.get_app()
        [app.include_router(r) for r in self.create_routers(settings)]

        return app

    @abstractmethod
    def default_impl(self) -> SETTINGS:
        pass

    @abstractmethod
    def integrity_errors_impl(self) -> SETTINGS:
        pass
