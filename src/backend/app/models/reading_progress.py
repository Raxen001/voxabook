import uuid
from sqlmodel import Field
from .base import Base

class readingProgress(Base , table = True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    book_id: uuid.UUID = Field(foreign_key="book.id")
    chapter_id: uuid.UUID = Field(foreign_key="chapter.id")
    progress_percentage: float