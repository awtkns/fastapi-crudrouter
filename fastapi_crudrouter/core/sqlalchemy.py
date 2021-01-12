from typing import Callable
from fastapi import Depends
from pydantic import BaseModel

from . import CRUDGenerator, NOT_FOUND


try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import DeclarativeMeta
except ImportError:
    sqlalchemy_installed = False
    Session = None
    DeclarativeMeta = None
else:
    sqlalchemy_installed = True


class SQLAlchemyCRUDRouter(CRUDGenerator):

    def __init__(self, schema: BaseModel, db_model: DeclarativeMeta, db: Session, *args, **kwargs):
        assert sqlalchemy_installed, "SQLAlchemy must be installed to use the SQLAlchemyCRUDRouter."

        self.db_model = db_model
        self.db_func = db
        self._primary_key: str = db_model.__table__.primary_key.columns.keys()[0]

        if 'prefix' not in kwargs:
            kwargs['prefix'] = db_model.__tablename__

        if 'create_schema' not in kwargs:
            kwargs['create_schema'] = self.schema_factory(schema, self._primary_key)

        super().__init__(schema, *args, **kwargs)

    def _get_all(self) -> Callable:
        def route(db: Session = Depends(self.db_func)):
            return db.query(self.db_model).all()

        return route

    def _get_one(self) -> Callable:
        def route(item_id, db: Session = Depends(self.db_func)):
            model = db.query(self.db_model).get(item_id)

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def _create(self) -> Callable:
        def route(model: self.create_schema, db: Session = Depends(self.db_func)):
            db_model = self.db_model(**model.dict())
            db.add(db_model)
            db.commit()
            db.refresh(db_model)

            return db_model

        return route

    def _update(self) -> Callable:
        def route(item_id: int, model: self.schema, db: Session = Depends(self.db_func)):
            db_model = self._get_one()(item_id, db)

            for key, value in model.dict(exclude={self._primary_key}).items():
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

            return self._get_all()(db)

        return route

    def _delete_one(self) -> Callable:
        def route(item_id: int, db: Session = Depends(self.db_func)):
            db_model = self._get_one()(item_id, db)
            db.delete(db_model)
            db.commit()

            return db_model

        return route