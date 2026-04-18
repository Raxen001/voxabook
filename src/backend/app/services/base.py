from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlmodel import Session, SQLModel

from app.crud.base import BaseCRUD
from app.schemas.common import PaginatedResponse

GenericModel = TypeVar("GenericModel", bound=SQLModel)
UpdateModelSchema = TypeVar("UpdateModelSchema", bound=BaseModel)
CreateModelSchema = TypeVar("CreateModelSchema", bound=BaseModel)


class BaseService(Generic[GenericModel, UpdateModelSchema, CreateModelSchema]):
    def __init__(
        self, session: Session, crud: BaseCRUD[GenericModel, UpdateModelSchema]
    ):
        self.session: Session = session
        self.crud: BaseCRUD[GenericModel, UpdateModelSchema] = crud

    def get(self, id: str) -> GenericModel | None:
        return self.crud.get(id=id)

    def list(
        self, offset: int = 0, limit: int = 100
    ) -> PaginatedResponse[GenericModel]:
        return self.crud.get_all(offset=offset, limit=limit)

    def create(self, create_schema_instance: CreateModelSchema) -> GenericModel:
        validated_from_create_schema = self.crud.model.model_validate(
            create_schema_instance
        )
        return self.crud.create(instance=validated_from_create_schema)

    def update(self, id: str, data: UpdateModelSchema) -> GenericModel | None:
        return self.crud.update(id=id, update_schema=data)

    def delete(self, id: str) -> GenericModel | None:
        return self.crud.delete(id=id)

    def filter(
        self,
        offset: int = 0,
        limit: int = 100,
        **kwargs: str | int | float | bool | None,
    ) -> list[GenericModel]:
        return self.crud.filter(offset=offset, limit=limit, **kwargs)
