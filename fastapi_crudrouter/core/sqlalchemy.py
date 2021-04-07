from typing import Any, Callable, List, Type, Generator, Optional

from fastapi import Depends, HTTPException

from . import CRUDGenerator, NOT_FOUND, _utils
from ._types import PAGINATION, PYDANTIC_SCHEMA as SCHEMA

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


class SQLAlchemyCRUDRouter(CRUDGenerator[SCHEMA]):
    def __init__(
        self,
        schema: Type[SCHEMA],
        db_model: Model,
        db: "Session",
        create_schema: Optional[Type[SCHEMA]] = None,
        update_schema: Optional[Type[SCHEMA]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: bool = True,
        get_one_route: bool = True,
        create_route: bool = True,
        update_route: bool = True,
        delete_one_route: bool = True,
        delete_all_route: bool = True,
        get_all_dependency: Optional[Callable] = None,
        get_one_dependency: Optional[Callable] = None,
        create_dependency: Optional[Callable] = None,
        update_dependency: Optional[Callable] = None,
        delete_one_dependency: Optional[Callable] = None,
        delete_all_dependency: Optional[Callable] = None,
        **kwargs: Any
    ) -> None:
        assert (
            sqlalchemy_installed
        ), "SQLAlchemy must be installed to use the SQLAlchemyCRUDRouter."

        self.db_model = db_model
        self.db_func = db
        self._pk: str = db_model.__table__.primary_key.columns.keys()[0]
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)
        self.get_all_dependency = get_all_dependency
        self.get_one_dependency = get_one_dependency
        self.create_dependency = create_dependency
        self.update_dependency = update_dependency
        self.delete_one_dependency = delete_one_dependency
        self.delete_all_dependency = delete_all_dependency

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
            dependency: Callable[..., Any] = Depends(self.get_all_dependency),
        ) -> List[Model]:
            skip, limit = pagination.get("skip"), pagination.get("limit")

            db_models: List[Model] = (
                db.query(self.db_model).limit(limit).offset(skip).all()
            )
            return db_models

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., Model]:
        def route(
            item_id: self._pk_type,
            db: Session = Depends(self.db_func),  # type: ignore
            dependency: Callable[..., Any] = Depends(self.get_one_dependency),
        ) -> Model:
            model: Model = db.query(self.db_model).get(item_id)

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., Model]:
        def route(
            model: self.create_schema,  # type: ignore
            db: Session = Depends(self.db_func),
            dependency: Callable[..., Any] = Depends(self.create_dependency),
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
            dependency: Callable[..., Any] = Depends(self.update_dependency),
        ) -> Model:
            try:
                db_model: Model = self._get_one()(item_id, db)

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
        def route(
            db: Session = Depends(self.db_func),
            dependency: Callable[..., Any] = Depends(self.delete_all_dependency),
        ) -> List[Model]:
            db.query(self.db_model).delete()
            db.commit()

            return self._get_all()(db=db, pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., Model]:
        def route(
            item_id: self._pk_type,
            db: Session = Depends(self.db_func),  # type: ignore
            dependency: Callable[..., Any] = Depends(self.delete_one_dependency),
        ) -> Model:
            db_model: Model = self._get_one()(item_id, db)
            db.delete(db_model)
            db.commit()

            return db_model

        return route
