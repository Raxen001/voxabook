import uuid

from sqlmodel import Field

from .base import Base


class Chapter(Base, table=True):
    title: str
    book_id: uuid.UUID = Field(foreign_key="book.id")
    chapter_index: int

