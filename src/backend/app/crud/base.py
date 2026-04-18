from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import ColumnElement, func
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, SQLModel, select

from app.exception import NotFoundError, UpdateFailedError
from app.schemas.common import PaginatedResponse

GenericModel = TypeVar("GenericModel", bound=SQLModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseCRUD(Generic[GenericModel, UpdateSchema]):
    session: Session
    model: type[GenericModel]

    def __init__(self, model: type[GenericModel], session: Session):
        super().__init__()
        self.session = session
        self.model = model

    def create(self, instance: GenericModel):
        self.session.add(instance=instance)
        self.session.commit()
        self.session.refresh(instance=instance)

        return instance

    def get(self, id: str):
        obj = self.session.get(self.model, id)

        if not obj:
            raise NotFoundError(str(self.model.__name__))

        return obj

    def get_all(self, offset: int = 0, limit: int = 100):
        count_statement = (
            select(func.count())
            .offset(offset=offset)
            .limit(limit=limit)
            .select_from(self.model)
        )
        try:
            count = self.session.exec(count_statement).one()
        except NoResultFound:
            raise NotFoundError(self.model.__name__)

        statement = select(self.model).offset(offset=offset).limit(limit=limit)
        rows = self.session.exec(statement=statement).all()

        return PaginatedResponse(data=list(rows), count=count)

    def update(self, id: str, update_schema: UpdateSchema):
        entity = self.get(id=id)

        if not entity:
            raise NotFoundError(str(self.model.__name__))

        update_data = update_schema.model_dump(exclude_unset=True)
        update_resp = entity.sqlmodel_update(update_data)

        if not update_resp:
            raise UpdateFailedError(str(self.model.__name__))

        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)

    def delete(self, id: str):
        entity = self.get(id=id)

        self.session.delete(entity)
        self.session.commit()

        return entity

    def filter(
        self,
        offset: int = 0,
        limit: int = 100,
        *column: ColumnElement[bool],
        **kwargs: Any
    ) -> list[Any]:
        statement = (
            select(self.model)
            .filter(*column)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
        )
        result = self.session.exec(statement=statement)

        return list(result)
