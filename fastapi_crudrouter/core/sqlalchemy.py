from typing import Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from . import CRUDGenerator, NOT_FOUND


class SQLAlchemyCRUDRouter(CRUDGenerator):
    # db_func = None

    def __init__(self, db_model, db, model, *args, **kwargs):
        self.db_model = db_model
        self.db_func = db

        super().__init__(model, *args, **kwargs)

    def get_all(self) -> Callable:
        def route(db: Session = Depends(self.db_func)):
            return db.query(self.db_model).all()

        return route

    def get_one(self) -> Callable:
        def route(item_id: int, db: Session = Depends(self.db_func)):
            model = db.query(self.db_model).get(item_id)

            if model:
                return model
            else:
                raise NOT_FOUND

        return route

    def create(self) -> Callable:
        def route(model: self.create_schema, db: Session = Depends(self.db_func)):
            db_model = self.db_model(**model.dict())
            db.add(db_model)
            db.commit()
            db.refresh(db_model)

            return db_model

        return route

    def update(self) -> Callable:
        def route(item_id: int, model: self.model_cls, db: Session = Depends(self.db_func)):
            db_model = self.get_one()(item_id, db)

            for key, value in model.dict(exclude={'id'}).items():
                if hasattr(db_model, key):
                    setattr(db_model, key, value)

            db.commit()
            db.refresh(db_model)

            return db_model

        return route

    def delete_all(self) -> Callable:
        def route(db: Session = Depends(self.db_func)):
            db.query(self.db_model).delete()
            db.commit()

            return self.get_all()(db)

        return route

    def delete_one(self) -> Callable:
        def route(item_id: int, db: Session = Depends(self.db_func)):
            db_model = self.get_one()(item_id, db)
            db.delete(db_model)
            db.commit()

            return db_model

        return route