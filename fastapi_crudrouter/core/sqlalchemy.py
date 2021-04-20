import typing
from datetime import datetime
from typing import Any, Callable, Dict, Generator, List
from typing import Optional, Type, Union, get_type_hints

from fastapi import Depends, HTTPException, Request

from . import CRUDGenerator, NOT_FOUND, _utils
from ._types import DEPENDENCIES, PAGINATION, PYDANTIC_SCHEMA as SCHEMA

try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import DeclarativeMeta as Model
    from sqlalchemy.exc import IntegrityError
except ImportError:
    Model: Any = None  # type: ignore
    sqlalchemy_installed = False
else:
    sqlalchemy_installed = True
    Session = Callable[..., Generator[Session, Any, None]]

FILTER = Dict[str, Optional[Union[int, str, datetime, None]]]


def schemas_args_factory(schema: Optional[Type[SCHEMA]]) -> Any:
    """
    Created the schema dependency to be used in the router
    """
    schema_typing = get_type_hints(schema)
    _str = "{}: Optional[{}] = None"
    args = (
        _str.format(k, v.__name__)
        for k, v in schema_typing.items()
        if v.__module__ != "typing"
    )
    args_str: str = ",".join(args)
    return_str = ", ".join(
        [
            "{}={}".format(k, k)
            for k, v in schema_typing.items()
            if v.__module__ != "typing"
        ]
    )

    func_code = "def tmp_function({0}) -> FILTER:return dict({1})"
    func_code = func_code.format(args_str, return_str)
    local_var = {"datetime": datetime, "FILTER": FILTER, "typing": typing}
    exec(func_code, globals(), local_var)
    tmp_function = local_var["tmp_function"]
    return tmp_function


class SQLAlchemyCRUDRouter(CRUDGenerator[SCHEMA]):
    def __init__(
        self,
        schema: Optional[Type[SCHEMA]],
        db_model: Model,
        db: "Session",
        create_schema: Optional[Type[SCHEMA]] = None,
        update_schema: Optional[Type[SCHEMA]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = True,
        **kwargs: Any
    ) -> None:
        assert (
            sqlalchemy_installed
        ), "SQLAlchemy must be installed to use the SQLAlchemyCRUDRouter."
        if schema is None:
            try:
                from pydantic_sqlalchemy import sqlalchemy_to_pydantic
            except ImportError:
                raise ValueError(
                    "Schema should not be None,or installed pydantic_sqlalchemy"
                )
            schema = sqlalchemy_to_pydantic(db_model)
        self.db_model = db_model
        self.db_func = db
        self._pk: str = db_model.__table__.primary_key.columns.keys()[0]
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        super().__init__(
            schema=schema,
            create_schema=create_schema,
            update_schema=update_schema,
            prefix=prefix or db_model.__tablename__,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs
        )

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[Model]]:
        def route(
            db: Session = Depends(self.db_func),
            pagination: PAGINATION = self.pagination,
            condition: FILTER = Depends(schemas_args_factory(self.schema)),
            request: Request = Request(scope={"type": "http"}),
        ) -> List[Model]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            effective_filter = {
                k: v for k, v in condition.items() if k in request.query_params.keys()
            }

            query = db.query(self.db_model).filter_by(**effective_filter)
            db_models: List[Model] = query.limit(limit).offset(skip).all()
            return db_models

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., Model]:
        def route(
            item_id: Optional[self._pk_type] = None,  # type: ignore
            db: Session = Depends(self.db_func),
            condition: FILTER = Depends(schemas_args_factory(self.schema)),
            request: Request = Request(scope={"type": "http"}),
        ) -> Model:
            effective_filter = {
                k: v for k, v in condition.items() if k in request.query_params.keys()
            }
            if item_id:
                effective_filter[self._pk] = item_id
            model: Model = db.query(self.db_model).filter_by(**effective_filter).first()

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., Model]:
        def route(
            model: self.create_schema,  # type: ignore
            db: Session = Depends(self.db_func),
        ) -> Model:
            try:
                db_model: Model = self.db_model(**model.dict())
                db.add(db_model)
                db.commit()
                db.refresh(db_model)
                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, "Key already exists")

        return route

    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., Model]:
        def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
            db: Session = Depends(self.db_func),
        ) -> Model:
            try:
                db_model: Model = self._get_one()(item_id, db, {})

                for key, value in model.dict(exclude={self._pk}).items():
                    if hasattr(db_model, key):
                        setattr(db_model, key, value)

                db.commit()
                db.refresh(db_model)

                return db_model
            except IntegrityError as e:
                db.rollback()
                raise HTTPException(422, ", ".join(e.args))

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[Model]]:
        def route(db: Session = Depends(self.db_func)) -> List[Model]:
            db.query(self.db_model).delete()
            db.commit()

            return self._get_all()(
                db=db, pagination={"skip": 0, "limit": None}, condition={}
            )

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., Model]:
        def route(
            item_id: self._pk_type, db: Session = Depends(self.db_func)  # type: ignore
        ) -> Model:
            db_model: Model = self._get_one()(item_id, db, {})
            db.delete(db_model)
            db.commit()

            return db_model

        return route
