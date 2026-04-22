
import uuid
from sqlmodel import Field
from .base import Base

class Book(Base, table=True):
    title: str
    isbn_id: str
    author: str | None = None
    publisher: str | None = None
    published_date: str | None = None
    description: str | None = None
    language: str | None = None
    page_count: int | None = None
    cover_url: str | None = None
    genre: str | None = None
