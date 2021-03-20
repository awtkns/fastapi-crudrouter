from typing import Callable, Generator, Any

from fastapi import Depends, HTTPException
from pydantic import BaseModel

from . import CRUDGenerator, NOT_FOUND, _utils

try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import DeclarativeMeta
    from sqlalchemy.exc import IntegrityError
except ImportError:
    sqlalchemy_installed = False
    Session = None
    DeclarativeMeta = None
else:
    sqlalchemy_installed = True


class SQLAlchemyCRUDRouter(CRUDGenerator):

    def __init__(self, schema: BaseModel, db_model: DeclarativeMeta, db: Callable[..., Generator[Session, Any, None]], *args, **kwargs):
        assert sqlalchemy_installed, "SQLAlchemy must be installed to use the SQLAlchemyCRUDRouter."

        self.db_model = db_model
        self.db_func = db
        self._pk: str = db_model.__table__.primary_key.columns.keys()[0]
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        if 'prefix' not in kwargs:
            kwargs['prefix'] = db_model.__tablename__

        if 'create_schema' not in kwargs:
            kwargs['create_schema'] = _utils.schema_factory(schema, self._pk)

        super().__init__(schema, *args, **kwargs)

    def _get_all(self) -> Callable:
        def route(db: Session = Depends(self.db_func), pagination: dict = self.pagination):
            skip, limit = pagination.get('skip'), pagination.get('limit')

            return db.query(self.db_model).limit(limit).offset(skip).all()

        return route

    def _get_one(self) -> Callable:
        def route(item_id: self._pk_type, db: Session = Depends(self.db_func)):
            model = db.query(self.db_model).get(item_id)

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(self) -> Callable:
        def route(model: self.create_schema, db: Session = Depends(self.db_func)):
            try:
                db_model = self.db_model(**model.dict())
                db.add(db_model)
                db.commit()
                db.refresh(db_model)
                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, 'Key already exists')

        return route

    def _update(self) -> Callable:
        def route(item_id: self._pk_type, model: self.update_schema, db: Session = Depends(self.db_func)):
            db_model = self._get_one()(item_id, db)

            for key, value in model.dict(exclude={self._pk}).items():
                if hasattr(db_model, key):
                    setattr(db_model, key, value)

            db.commit()
            db.refresh(db_model)

            return db_model

        return route

    def _delete_all(self) -> Callable:
        def route(db: Session = Depends(self.db_func)):
            db.query(self.db_model).delete()
            db.commit()

            return self._get_all()(db=db, pagination={
                'skip': 0,
                'limit': None
            })

        return route

    def _delete_one(self) -> Callable:
        def route(item_id: self._pk_type, db: Session = Depends(self.db_func)):
            db_model = self._get_one()(item_id, db)
            db.delete(db_model)
            db.commit()

            return db_model

        return route
