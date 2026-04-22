
import uuid
from sqlmodel import Field, SQLModel

class UserBook(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    book_id: uuid.UUID = Field(foreign_key="book.id", primary_key=True)
