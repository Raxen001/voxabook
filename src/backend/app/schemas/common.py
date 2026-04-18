from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class PageParams(BaseModel):
    skip: int = Field(default=0)
    limit: int = Field(default=10, gt=0, le=255)


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    count: int
