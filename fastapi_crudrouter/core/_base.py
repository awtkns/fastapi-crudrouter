from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, List, Optional, Type, Union

from fastapi import APIRouter, HTTPException, status
from fastapi.types import DecoratedCallable

from ._types import T, DEPENDENCIES
from ._utils import pagination_factory, schema_factory

NOT_FOUND = HTTPException(404, "Item not found")


class CRUDGenerator(Generic[T], APIRouter, ABC):
    schema: Type[T]
    create_schema: Type[T]
    update_schema: Type[T]
    _base_path: str = "/"

    def __init__(
        self,
        schema: Type[T],
        create_schema: Optional[Type[T]] = None,
        update_schema: Optional[Type[T]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = True,
        create_status_code: Optional[int] = status.HTTP_201_CREATED,
        get_all_status_code: Optional[int] = status.HTTP_200_OK,
        get_one_status_code: Optional[int] = status.HTTP_200_OK,
        update_status_code: Optional[int] = status.HTTP_200_OK,
        delete_status_code: Optional[int] = status.HTTP_200_OK,
        **kwargs: Any,
    ) -> None:

        self.schema = schema
        self.pagination = pagination_factory(max_limit=paginate)
        self._pk: str = self._pk if hasattr(self, "_pk") else "id"
        self.create_schema = (
            create_schema
            if create_schema
            else schema_factory(self.schema, pk_field_name=self._pk, name="Create")
        )
        self.update_schema = (
            update_schema
            if update_schema
            else schema_factory(self.schema, pk_field_name=self._pk, name="Update")
        )

        prefix = str(prefix if prefix else self.schema.__name__).lower()
        prefix = self._base_path + prefix.strip("/")
        tags = tags or [prefix.strip("/").capitalize()]

        super().__init__(prefix=prefix, tags=tags, **kwargs)

        if get_all_route:
            self._add_api_route(
                "",
                self._get_all(),
                methods=["GET"],
                response_model=Optional[List[self.schema]],  # type: ignore
                summary="Get All",
                dependencies=get_all_route,
                status_code=get_all_status_code,
            )

        if create_route:
            self._add_api_route(
                "",
                self._create(),
                methods=["POST"],
                response_model=None if create_status_code == 204 else self.schema,
                summary="Create One",
                dependencies=create_route,
                status_code=create_status_code,
            )

        if delete_all_route:
            self._add_api_route(
                "",
                self._delete_all(),
                methods=["DELETE"],
                response_model=Optional[List[self.schema]],  # type: ignore
                summary="Delete All",
                dependencies=delete_all_route,
            )

        if get_one_route:
            self._add_api_route(
                "/{item_id}",
                self._get_one(),
                methods=["GET"],
                response_model=self.schema,
                summary="Get One",
                dependencies=get_one_route,
                error_responses=[NOT_FOUND],
                status_code=get_one_status_code,
            )

        if update_route:
            self._add_api_route(
                "/{item_id}",
                self._update(),
                methods=["PUT"],
                response_model=None if update_status_code == 204 else self.schema,
                summary="Update One",
                dependencies=update_route,
                error_responses=[NOT_FOUND],
                status_code=update_status_code,
            )

        if delete_one_route:
            self._add_api_route(
                "/{item_id}",
                self._delete_one(),
                methods=["DELETE"],
                response_model=None if delete_status_code == 204 else self.schema,
                summary="Delete One",
                dependencies=delete_one_route,
                error_responses=[NOT_FOUND],
                status_code=delete_status_code,
            )

    def _add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        dependencies: Union[bool, DEPENDENCIES],
        error_responses: Optional[List[HTTPException]] = None,
        status_code: Optional[int] = 200,
        **kwargs: Any,
    ) -> None:
        dependencies = [] if isinstance(dependencies, bool) else dependencies
        responses: Any = (
            {err.status_code: {"detail": err.detail} for err in error_responses}
            if error_responses
            else None
        )

        super().add_api_route(
            path, endpoint, dependencies=dependencies, responses=responses, status_code=status_code, **kwargs
        )

    def api_route(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Overrides and exiting route if it exists"""
        methods = kwargs["methods"] if "methods" in kwargs else ["GET"]
        self.remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def get(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["Get"])
        return super().get(path, *args, **kwargs)

    def post(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        methods_ = set(methods)

        for route in self.routes:
            if (
                route.path == f"{self.prefix}{path}"  # type: ignore
                and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    @abstractmethod
    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    @abstractmethod
    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        raise NotImplementedError

    def _raise(self, e: Exception, status_code: int = 422) -> HTTPException:
        raise HTTPException(422, ", ".join(e.args)) from e

    @staticmethod
    def get_routes() -> List[str]:
        return ["get_all", "create", "delete_all", "get_one", "update", "delete_one"]
