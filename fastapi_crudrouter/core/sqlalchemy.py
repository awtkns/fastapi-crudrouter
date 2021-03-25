from typing import Any, Callable, List, Type, TypeVar

from fastapi import Depends, HTTPException

from . import CRUDGenerator, NOT_FOUND, T, _utils

try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import DeclarativeMeta
    from sqlalchemy.exc import IntegrityError
except ImportError:
    sqlalchemy_installed = False
else:
    sqlalchemy_installed = True
TM = TypeVar("TM", bound="DeclarativeMeta")


class SQLAlchemyCRUDRouter(CRUDGenerator[T]):
    def __init__(
        self,
        schema: Type[T],
        db_model: Type[TM],
        db: "Session",
        *args: Any,
        **kwargs: Any
    ) -> None:
        assert (
            sqlalchemy_installed
        ), "SQLAlchemy must be installed to use the SQLAlchemyCRUDRouter."

        self.db_model = db_model
        self.db_func = db
        self._pk: str = db_model.__table__.primary_key.columns.keys()[0]
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        if "prefix" not in kwargs:
            kwargs["prefix"] = db_model.__tablename__

        if "create_schema" not in kwargs:
            kwargs["create_schema"] = _utils.schema_factory(schema, self._pk)

        super().__init__(schema, *args, **kwargs)

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[TM]]:
        def route(
            db: Session = Depends(self.db_func),
            pagination: dict = self.pagination,  # type: ignore
        ) -> List[TM]:
            skip, limit = pagination.get("skip"), pagination.get("limit")

            db_models: List[TM] = (
                db.query(self.db_model).limit(limit).offset(skip).all()
            )
            return db_models

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., TM]:
        def route(
            item_id: self._pk_type, db: Session = Depends(self.db_func)  # type: ignore
        ) -> TM:
            model: TM = db.query(self.db_model).get(item_id)

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., TM]:
        def route(
            model: self.create_schema,  # type: ignore
            db: Session = Depends(self.db_func),
        ) -> TM:
            try:
                db_model: TM = self.db_model(**model.dict())
                db.add(db_model)
                db.commit()
                db.refresh(db_model)
                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, "Key already exists")

        return route

    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., TM]:
        def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
            db: Session = Depends(self.db_func),
        ) -> TM:
            try:
                db_model: TM = self._get_one()(item_id, db)

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

    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[TM]]:
        def route(db: Session = Depends(self.db_func)) -> List[TM]:
            db.query(self.db_model).delete()
            db.commit()

            return self._get_all()(db=db, pagination={"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., TM]:
        def route(
            item_id: self._pk_type, db: Session = Depends(self.db_func)  # type: ignore
        ) -> TM:
            db_model: TM = self._get_one()(item_id, db)
            db.delete(db_model)
            db.commit()

            return db_model

        return route
