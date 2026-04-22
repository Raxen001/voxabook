from .base import Base

class User(Base , table = True):
    clerk_user_id: str
    name: str